CREATE TABLE IF NOT EXISTS mainmenu (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS shop_menu(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL,
    table_n text NOT NULL
);

CREATE TABLE IF NOT EXISTS products(
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    price int NOT NULL,
    descript text NOT NULL,
    table_n text NOT NULL,
    product_photo text NOT NULL,
    post_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    login text NOT NULL,
    password text NOT NULL,
    phone text NOT NULL,
    avatar BLOB DEFAULT NULL
);
