-- Opcional: crear la base de datos
CREATE DATABASE IF NOT EXISTS flor_canela_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE flor_canela_db;

-- 1. Tabla ROLES
CREATE TABLE roles (
    id_rol INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Tabla USUARIOS
CREATE TABLE usuarios (
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_rol INT UNSIGNED NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    area_trabajo VARCHAR(100),
    foto_url VARCHAR(255),
    estado ENUM('activo','inactivo') NOT NULL DEFAULT 'activo',
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso DATETIME NULL,
    CONSTRAINT fk_usuarios_roles
        FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Tabla ACCESOS_USUARIOS (historial de logins)
CREATE TABLE accesos_usuarios (
    id_acceso INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    fecha_login DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip VARCHAR(45),
    user_agent VARCHAR(255),
    CONSTRAINT fk_accesos_usuarios_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Tabla TAREAS
CREATE TABLE tareas (
    id_tarea INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_tarea_padre INT UNSIGNED NULL,
    id_creador INT UNSIGNED NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_inicio_prog DATETIME NULL,
    fecha_fin_prog DATETIME NULL,
    fecha_fin_real DATETIME NULL,
    prioridad ENUM('baja','media','alta','critica') NOT NULL DEFAULT 'media',
    estado ENUM('pendiente','en_progreso','completada','cancelada')
        NOT NULL DEFAULT 'pendiente',
    porcentaje_avance TINYINT UNSIGNED NOT NULL DEFAULT 0,
    es_recurrente TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT fk_tareas_creador
        FOREIGN KEY (id_creador) REFERENCES usuarios(id_usuario),
    CONSTRAINT fk_tareas_padre
        FOREIGN KEY (id_tarea_padre) REFERENCES tareas(id_tarea)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Tabla ASIGNACIONES_TAREA
CREATE TABLE asignaciones_tarea (
    id_asignacion INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_tarea INT UNSIGNED NOT NULL,
    id_usuario INT UNSIGNED NOT NULL,
    fecha_asignacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    CONSTRAINT fk_asignacion_tarea
        FOREIGN KEY (id_tarea) REFERENCES tareas(id_tarea),
    CONSTRAINT fk_asignacion_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Tabla HISTORIAL_ESTADOS_TAREA
CREATE TABLE historial_estados_tarea (
    id_historial INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_tarea INT NULL,
    estado_anterior ENUM('pendiente','en_progreso','completada','cancelada'),
    estado_nuevo ENUM('pendiente','en_progreso','completada','cancelada')
        NOT NULL,
    fecha_cambio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT UNSIGNED NOT NULL,
    comentario VARCHAR(255),
    CONSTRAINT fk_historial_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Tabla COMENTARIOS_TAREA
CREATE TABLE comentarios_tarea (
    id_comentario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_tarea INT UNSIGNED NOT NULL,
    id_usuario INT UNSIGNED NOT NULL,
    texto TEXT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comentario_tarea
        FOREIGN KEY (id_tarea) REFERENCES tareas(id_tarea),
    CONSTRAINT fk_comentario_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Tabla RECURSOS
CREATE TABLE recursos (
    id_recurso INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    tipo ENUM('insumo','herramienta','maquinaria','otro') NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL,
    cantidad_disponible DECIMAL(10,2) NOT NULL DEFAULT 0,
    ubicacion VARCHAR(100),
    estado ENUM('operativo','mantenimiento','baja') NOT NULL DEFAULT 'operativo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Tabla TAREAS_RECURSOS (consumo de recursos por tarea)
CREATE TABLE tareas_recursos (
    id_tarea_recurso INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_tarea INT UNSIGNED NOT NULL,
    id_recurso INT UNSIGNED NOT NULL,
    cantidad_usada DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_tarea_recurso_tarea
        FOREIGN KEY (id_tarea) REFERENCES tareas(id_tarea),
    CONSTRAINT fk_tarea_recurso_recurso
        FOREIGN KEY (id_recurso) REFERENCES recursos(id_recurso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Tabla MANTENIMIENTOS_RECURSO
CREATE TABLE mantenimientos_recurso (
    id_mantenimiento INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_recurso INT UNSIGNED NOT NULL,
    fecha_programada DATE NOT NULL,
    fecha_real DATE NULL,
    tipo VARCHAR(80) NOT NULL,
    descripcion TEXT,
    estado ENUM('pendiente','realizado','cancelado')
        NOT NULL DEFAULT 'pendiente',
    CONSTRAINT fk_mantenimiento_recurso
        FOREIGN KEY (id_recurso) REFERENCES recursos(id_recurso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. Tabla NOTIFICACIONES
CREATE TABLE notificaciones (
    id_notificacion INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    id_tarea INT UNSIGNED NULL,
    id_recurso INT UNSIGNED NULL,
    tipo ENUM('tarea_asignada','proxima_vencer','vencida',
              'bajo_stock','mantenimiento') NOT NULL,
    mensaje VARCHAR(255) NOT NULL,
    fecha_envio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    leida TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT fk_notif_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    CONSTRAINT fk_notif_tarea
        FOREIGN KEY (id_tarea) REFERENCES tareas(id_tarea),
    CONSTRAINT fk_notif_recurso
        FOREIGN KEY (id_recurso) REFERENCES recursos(id_recurso)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS permisos (
  id_permiso INT AUTO_INCREMENT PRIMARY KEY,
  clave VARCHAR(80) NOT NULL UNIQUE,
  descripcion VARCHAR(255) NULL,
  modulo VARCHAR(50) NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rol_permisos (
  id_rol INT UNSIGNED NOT NULL,
  id_permiso INT NOT NULL,
  PRIMARY KEY (id_rol, id_permiso),
  CONSTRAINT fk_rp_rol FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE CASCADE,
  CONSTRAINT fk_rp_permiso FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS menu_items (
  id_menu INT AUTO_INCREMENT PRIMARY KEY,
  clave VARCHAR(80) NOT NULL UNIQUE,
  label VARCHAR(80) NOT NULL,
  path VARCHAR(120) NOT NULL,
  icon VARCHAR(40) NULL,
  orden INT NOT NULL DEFAULT 1,
  permiso_clave VARCHAR(80) NULL, -- si es NULL, es público para cualquier logueado
  activo TINYINT NOT NULL DEFAULT 1
);

