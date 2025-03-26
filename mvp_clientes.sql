CREATE DATABASE IF NOT EXISTS mvp_clientes;
USE mvp_clientes;

-- Tabla para almacenar los usuarios del sistema
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- Almacenará la contraseña hasheada
    rol ENUM('agente_cs', 'team_leader', 'gerente') NOT NULL, -- Roles en minúsculas
    team_leader_id INT NULL, -- Solo aplica para Agentes CS, indica su Team Leader
    FOREIGN KEY (team_leader_id) REFERENCES usuarios(id)
);

-- Tabla para almacenar los datos de los clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    creado_por INT NOT NULL, -- ID del usuario que creó el registro
    name INT,
    phone BIGINT,
    address VARCHAR(255),
    email VARCHAR(255),
    bank_account BIGINT, -- Cambiado de CTA a bank_account
    transfer VARCHAR(255),
    pin INT,
    offer VARCHAR(255),
    taxes VARCHAR(255),
    ssn BIGINT,
    tax_id BIGINT,
    itin BIGINT,
    driving_license VARCHAR(255),
    driving_license_expiration DATE,
    passport VARCHAR(255),
    passport_expiration DATE,
    birthdate DATE,
    billing_card BIGINT,
    name_card VARCHAR(255),
    zip INT,
    cvv INT,
    expiration_card DATE,
    state VARCHAR(255), -- Nuevo campo agregado
    city VARCHAR(255), -- Nuevo campo agregado
    FOREIGN KEY (creado_por) REFERENCES usuarios(id)
);

select * from usuarios;
select * from clientes;

ALTER TABLE clientes
MODIFY COLUMN name VARCHAR(255);