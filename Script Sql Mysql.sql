-- Script para crear la base de datos y la tabla en MySQL
CREATE DATABASE IF NOT EXISTS formularios_db;
USE formularios_db;

CREATE TABLE IF NOT EXISTS formularios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    intereses VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL
);

