from owlready2 import *

# 1. Cargar la ontología (ej. desde un archivo local)
onto = get_ontology("ontologia-ia-anahuac-ejemplo-1.owx").load()

# 2. Extraer (listar) las Clases
for clase in onto.classes():
    print(f"Clase: {clase.name}")

# 3. Extraer las Propiedades de Objeto (relaciones entre individuos)
for prop_obj in onto.object_properties():
    print(f"Propiedad de Objeto: {prop_obj.name}")

# 4. Extraer las Propiedades de Datos (atributos con valores literales)
for prop_dato in onto.data_properties():
    print(f"Propiedad de Datos: {prop_dato.name}")

# 5. Extraer los Individuos (instancias de clases)
for individuo in onto.individuals():
    print(f"Individuo: {individuo.name} -> Clase: {individuo.__class__.__name__}")