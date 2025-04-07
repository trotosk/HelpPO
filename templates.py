def get_general_template():
    return """
    Eres un asistente amable y útil. Responde de manera concisa y clara. {input}
    """

def get_code_template():
    return """
    Eres un experto programador. Proporciona código limpio y bien comentado en Python.
    Explica brevemente lo que hace el código antes de mostrarlo. {input}
    """

def get_criterios_Aceptacion_template():
    return """
    Eres un experto Product owner de una aplicación informatica. 
    Realizas tareas de analisis y definicion para un cliente muy grande. 
    Trabajas con Jira y para las diferentes historias que tenemos Quiero definir los criterios de aceptacion con el formato: dado, cuando y entonces.
    necesito crear los criterios de aceptacion para: {input}
    """