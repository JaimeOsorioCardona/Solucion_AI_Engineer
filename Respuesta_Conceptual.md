# Conceptual Answers

## 1. Conexión de Copiloto al Repositorio y Buenas Prácticas

**Conexión:**
La mejor manera es integrar herramientas nativas como GitHub Copilot o Cursor directamente en el IDE, asegurando permisos de lectura limitados y controlados. No se debe otorgar acceso de escritura directo a la rama principal (main/master).

**Buenas Prácticas:**
- **Revisión Obligatoria (Code Review):** Todo código generado por IA debe pasar por un Pull Request revisado por un humano.
- **Contexto Limitado:** No alimentar a la IA con secretos, llaves de API o datos sensibles de clientes (PII).
- **Linters y Tests:** Usar hooks de pre-commit y CI/CD robustos para validar que el código generado cumpla con los estándares del proyecto antes de ser integrado.

## 2. Mantener el Conocimiento y Control del Negocio

Para no convertirse en "copiadores de código" y perder el entendimiento del sistema:
- **La Regla del "Por Qué":** El desarrollador debe ser capaz de explicar *por qué* la solución de la IA funciona y *por qué* es la mejor opción. Si no puede explicarlo, no debe commitearlo.
- **Documentación Viva:** Usar la IA para generar documentación que explique la lógica de negocio, no solo el código.
- **Refactoring Manual:** Dedicar tiempo a refactorizar o reescribir partes críticas manualmente para mantener la agilidad mental y el conocimiento profundo de la arquitectura.
- **Pair Programming con IA:** Tratas a la IA como un junior o un par: tú diriges la estrategia, ella ejecuta la táctica.

## 3. ¿Qué es MCP y sus Casos de Uso?

**MCP (Model Context Protocol):**
Es un estándar abierto que permite a los asistentes de IA interactuar con datos y herramientas externas de manera segura y estructurada. Estandariza cómo una IA "ve" y "toca" el mundo exterior (bases de datos, sistemas de archivos, APIs).

**Casos de Uso Relevantes:**
- **Conexión a Bases de Datos:** Permitir que una IA consulte una base de datos SQL segura para responder preguntas de negocio sin exponer credenciales directamente en el prompt.
- **Gestión de Archivos:** Permitir que un agente edite código en un repositorio local de manera controlada (como lo que estamos haciendo ahora).
- **Integración de Herramientas Internas:** Conectar un chatbot de soporte a herramientas internas de gestión de usuarios o tickets mediante un protocolo común.

## 4. Fortalezas y Debilidades de la IA en Desarrollo

**Fortalezas:**
- **Productividad en Boilerplate:** Excelente para generar estructuras repetitivas, tests unitarios y documentación básica.
- **Patrones Comunes:** Conoce casi todos los algoritmos y patrones de diseño estándar.
- **Búsqueda Semántica:** Capacidad de entender "qué hace este error" mejor que una búsqueda por palabras clave.

**Debilidades:**
- **Alucinaciones:** Puede inventar librerías, métodos o versiones de dependencias que no existen o son incompatibles.
- **Contexto Limitado:** A menudo pierde el hilo en bases de código muy grandes o arquitecturas distribuidas complejas si no se le alimenta el contexto correcto.
- **Falta de Juicio Arquitectónico:** Tiende a optimizar localmente (una función) sin ver el impacto global (arquitectura del sistema), creando deuda técnica a largo plazo.

**Mitigación:**
- Usar IaC (Infrastructure as Code) y validación estática.
- Mantener a los humanos en el loop de diseño arquitectónico.
- Verificación constante a través de tests automatizados (TDD es vital al usar IA).
