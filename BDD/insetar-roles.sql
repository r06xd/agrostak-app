#Creacion de roles
INSERT INTO roles(nombre, descripcion) VALUES
('Administrador','Acceso total'),
('Supervisor','Supervisa tareas'),
('Trabajador','Ejecuta tareas');

#Crear los permisos
INSERT INTO permisos (clave, descripcion, modulo) VALUES
('USUARIOS_LISTAR','Listar usuarios','identity'),
('USUARIOS_CREAR','Crear usuarios','identity'),
('USUARIOS_EDITAR','Editar usuarios','identity'),
('USUARIOS_ELIMINAR','Eliminar usuarios','identity'),
('TAREAS_LISTAR','Listar tareas','tasks'),
('TAREAS_CREAR','Crear tareas','tasks'),
('TAREAS_EDITAR','Editar tareas','tasks'),
('TAREAS_ASIGNAR','Asignar tareas','tasks'),
('RECURSOS_CRUD','Gestionar recursos','resources'),
('REPORTES_VER','Ver reportes','reports')
ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion), modulo=VALUES(modulo);

#Parametrizacion de permisos a cada rol
-- ADMIN: todo
INSERT IGNORE INTO rol_permisos (id_rol, id_permiso)
SELECT 1, id_permiso FROM permisos;

-- SUPERVISOR: tareas + recursos + reportes
INSERT IGNORE INTO rol_permisos (id_rol, id_permiso)
SELECT 2, id_permiso FROM permisos
WHERE clave IN ('TAREAS_LISTAR','TAREAS_CREAR','TAREAS_EDITAR','TAREAS_ASIGNAR','RECURSOS_CRUD','REPORTES_VER');

-- TRABAJADOR: tareas listar/editar (luego limitas por asignación en service)
INSERT IGNORE INTO rol_permisos (id_rol, id_permiso)
SELECT 3, id_permiso FROM permisos
WHERE clave IN ('TAREAS_LISTAR','TAREAS_EDITAR');

INSERT INTO menu_items (clave,label,path,icon,orden,permiso_clave,activo) VALUES
('menu_usuarios','Usuarios','/usuarios','users',1,'USUARIOS_LISTAR',1),
('menu_tareas','Tareas','/tareas','checklist',2,'TAREAS_LISTAR',1),
('menu_recursos','Recursos','/recursos','box',3,'RECURSOS_CRUD',1),
('menu_reportes','Reportes','/reportes','chart',4,'REPORTES_VER',1)
ON DUPLICATE KEY UPDATE label=VALUES(label), path=VALUES(path), icon=VALUES(icon), orden=VALUES(orden), permiso_clave=VALUES(permiso_clave), activo=VALUES(activo);
