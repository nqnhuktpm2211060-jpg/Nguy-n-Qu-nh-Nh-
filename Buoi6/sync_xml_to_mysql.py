
"""
sync_xml_to_mysql.py
Usage:
    python sync_xml_to_mysql.py --xml supplier.xml --xsd supplier.xsd
"""

import argparse, sys
from decimal import Decimal, InvalidOperation
from lxml import etree
import mysql.connector
from mysql.connector import errorcode

# --------- Cấu hình DB (chỉnh tại đây nếu cần) ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",        
    "database": "supplier_sync"
}


CREATE_CATEGORIES_SQL = """
CREATE TABLE IF NOT EXISTS categories (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

CREATE_PRODUCTS_SQL = """
CREATE TABLE IF NOT EXISTS products (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(12,2) NOT NULL,
  currency VARCHAR(10) NOT NULL,
  stock INT NOT NULL,
  category_id VARCHAR(64) NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

def load_xml(path):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        return etree.parse(path, parser)
    except Exception as e:
        print(f"[ERROR] Parse XML failed: {e}")
        sys.exit(2)

def load_xsd(path):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        return etree.parse(path, parser)
    except Exception as e:
        print(f"[ERROR] Parse XSD failed: {e}")
        sys.exit(2)

def validate_xml(xml_doc, xsd_doc):
    try:
        schema = etree.XMLSchema(xsd_doc)
    except Exception as e:
        print(f"[ERROR] Build XMLSchema failed: {e}")
        sys.exit(2)
    valid = schema.validate(xml_doc)
    if valid:
        return True, None
    else:
        errors = []
        for err in schema.error_log:
            errors.append((err.line, err.column, err.message))
        return False, errors

def connect_db(cfg):
    try:
        return mysql.connector.connect(**cfg)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            # try to create db
            try:
                tmp = cfg.copy()
                dbname = tmp.pop("database")
                conn_tmp = mysql.connector.connect(**tmp)
                cur = conn_tmp.cursor()
                cur.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                conn_tmp.commit()
                cur.close()
                conn_tmp.close()
                print("[INFO] Database created, reconnecting...")
                return mysql.connector.connect(**cfg)
            except Exception as e:
                print(f"[ERROR] Create DB failed: {e}")
                sys.exit(3)
        else:
            print(f"[ERROR] DB connection error: {err}")
            sys.exit(3)

def create_tables(conn):
    cur = conn.cursor()
    cur.execute(CREATE_CATEGORIES_SQL)
    cur.execute(CREATE_PRODUCTS_SQL)
    conn.commit()
    cur.close()

def parse_and_upsert(xml_doc, conn):
    root = xml_doc.getroot()
    # categories
    cats = []
    for c in root.xpath("/catalog/categories/category"):
        cid = c.get("id")
        name = (c.text or "").strip()
        if cid:
            cats.append((cid, name))
    # products
    prods = []
    for p in root.xpath("/catalog/products/product"):
        pid = p.get("id")
        catref = p.get("categoryRef")
        name = (p.findtext("name") or "").strip()
        price_text = (p.findtext("price") or "").strip()
        currency = (p.find("price").get("currency") if p.find("price") is not None else "")
        stock_text = (p.findtext("stock") or "0").strip()
        # validate numeric
        try:
            price_val = Decimal(price_text)
        except (InvalidOperation, TypeError):
            print(f"[WARN] product {pid}: invalid price '{price_text}' — skip")
            continue
        try:
            stock_val = int(stock_text)
        except:
            print(f"[WARN] product {pid}: invalid stock '{stock_text}' — skip")
            continue
        prods.append((pid, name, float(price_val), currency, stock_val, catref))

    cur = conn.cursor()
    # upsert categories
    cat_sql = "INSERT INTO categories (id, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name)"
    for cid, cname in cats:
        cur.execute(cat_sql, (cid, cname))
    # upsert products
    prod_sql = ("INSERT INTO products (id, name, price, currency, stock, category_id) "
                "VALUES (%s, %s, %s, %s, %s, %s) "
                "ON DUPLICATE KEY UPDATE name=VALUES(name), price=VALUES(price), currency=VALUES(currency), stock=VALUES(stock), category_id=VALUES(category_id)")
    for row in prods:
        cur.execute(prod_sql, row)

    conn.commit()
    cur.close()
    return len(cats), len(prods)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml", required=True)
    parser.add_argument("--xsd", required=True)
    args = parser.parse_args()

    print("[STEP] Load XML")
    xml_doc = load_xml(args.xml)
    print("[STEP] Load XSD")
    xsd_doc = load_xsd(args.xsd)

    print("[STEP] Validate XML")
    ok, errs = validate_xml(xml_doc, xsd_doc)
    if not ok:
        print("[ERROR] XML invalid. Details:")
        for line, col, msg in errs:
            print(f" - Line {line}, Col {col}: {msg}")
        sys.exit(4)
    print("[OK] XML valid")

    print("[STEP] Connect DB")
    conn = connect_db(DB_CONFIG)
    print("[OK] Connected")

    print("[STEP] Create tables")
    create_tables(conn)
    print("[OK] Tables ready")

    print("[STEP] Parse & upsert data")
    cats_count, prods_count = parse_and_upsert(xml_doc, conn)
    print(f"[OK] inserted/updated {cats_count} categories and {prods_count} products")

    conn.close()
    print("Done.")

if __name__ == "__main__":
    main()
