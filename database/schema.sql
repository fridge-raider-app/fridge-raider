CREATE DATABASE fridge_raider;
USE fridge_raider;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  hashed_password BLOB
);

CREATE TABLE user_favourites (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  recipe_name VARCHAR(255) NOT NULL,
  recipe_source VARCHAR(255),
  recipe_url VARCHAR(255) NOT NULL,
  image_url TEXT NOT NULL,

  FOREIGN KEY (user_id) REFERENCES users (id)
);
