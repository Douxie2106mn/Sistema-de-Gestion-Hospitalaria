SELECT event_manipulation, action_statement
FROM information_schema.triggers
WHERE event_object_table = 'pacientes';

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'auditoria_consultas';


SELECT*FROM consultas

SELECT*FROM pacientes;
SELECT*FROM medicos;

SELECT*FROM consultas;
SELECT*FROM departamentos;
SELECT*FROM historial_medico;
SELECT*FROM usuarios;

SELECT*FROM auditoria_consultas;
SELECT*FROM auditoria_pacientes;
