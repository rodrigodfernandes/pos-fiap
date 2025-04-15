-- 1. Insert into Color table (Inserção na tabela de Cores)
INSERT INTO color (name) VALUES
('TINTA'),
('BRANCA E ROSADA');


-- 2. Insert into Kind table (Inserção na tabela de Tipos)
INSERT INTO kind (name) VALUES
('Viniferas'),
('Americanas e Hibridas'),
('Uvas de mesa'),
('Sem classificação');

-- 3. Insert into Wine Derivative Type table (Inserção na tabela de Tipo de Vinhos e Derivados)
INSERT INTO wine_derivative_type (name) VALUES
('VINHO DE MESA'),
('VINHO FINO DE MESA'),
('VINHO FRIZANTE'),
('VINHO ORGÂNICO'),
('VINHO ESPECIAL'),
('ESPUMANTES'),
('SUCO DE UVAS'),
('SUCO DE UVAS CONCENTRADO'),
('OUTROS PRODUTOS COMERCIALIZADOS');


-- 4. Insert into Grape Type table (Inserção na tabela de Tipo de Uva)
INSERT INTO grape_type (name) VALUES
('Vitis vinifera'),
('Vitis labrusca'),
('Vitis bourquina'),
('Uvas híbridas'),
('Não especificado');