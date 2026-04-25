import streamlit as st
import pandas as pd
import numpy as np
import libreria_funciones_proyecto1 as lib1
import libreria_clases_proyecto1 as lib

# Ejercicio 1: clases
# Clase para representar un movimiento
class Movimiento:
    def __init__(self, concepto, tipo, valor):
        self.concepto = concepto
        self.tipo = tipo
        self.valor = valor

# Clase para manejar el flujo de caja
class FlujoCaja:
    def __init__(self):
        self.movimientos = []

    def agregar_movimiento(self, movimiento):
        self.movimientos.append(movimiento)

    def obtener_dataframe(self):
        data = [{
            "Concepto": m.concepto,
            "Tipo": m.tipo,
            "Valor": m.valor
        } for m in self.movimientos]
        return pd.DataFrame(data)

    def total_ingresos(self):
        return sum(m.valor for m in self.movimientos if m.tipo == "Ingreso")

    def total_gastos(self):
        return sum(m.valor for m in self.movimientos if m.tipo == "Gasto")

    def saldo(self):
        return self.total_ingresos() - self.total_gastos()

# Ejercicio 2: clases
class RegistroVentas:
    def __init__(self):
        self.nombres = np.array([])
        self.categorias = np.array([])
        self.precios = np.array([])
        self.cantidades = np.array([])
        self.totales = np.array([])

    def agregar_registro(self, nombre, categoria, precio, cantidad):
        total = precio * cantidad

        self.nombres = np.append(self.nombres, nombre)
        self.categorias = np.append(self.categorias, categoria)
        self.precios = np.append(self.precios, precio)
        self.cantidades = np.append(self.cantidades, cantidad)
        self.totales = np.append(self.totales, total)

    def obtener_dataframe(self):
        return pd.DataFrame({
            "Producto": self.nombres,
            "Categoría": self.categorias,
            "Precio": self.precios,
            "Cantidad": self.cantidades,
            "Total": self.totales
        })
    
# Ejercicio 3: clases
# Clase para gestionar ejecuciones
class GestorROI:
    def __init__(self):
        self.historial = []

    def ejecutar_funcion(self, ganancia, inversion):
        resultado = lib1.calcular_roi(ganancia, inversion)
        
        registro = {
            "Ganancia Neta": ganancia,
            "Inversión": inversion,
            "ROI (%)": resultado["roi_pct"]
        }
        
        self.historial.append(registro)
        return resultado

    def obtener_historial(self):
        return pd.DataFrame(self.historial)


# Ejercicio 4: clases
# Clase gestora para CRUD usando clase real
class GestorInventario:
    def __init__(self):
        self.productos = []

    # CREATE
    def crear(self, nombre, costo, precio, stock, stock_min):
        producto = lib.InventarioProducto(nombre, costo, precio, stock, stock_min)
        self.productos.append(producto)

    # READ
    def leer(self):
        return pd.DataFrame([p.resumen() for p in self.productos])

    # UPDATE
    def actualizar(self, index, nombre, costo, precio, stock, stock_min):
        self.productos[index] = lib.InventarioProducto(nombre, costo, precio, stock, stock_min)

    # DELETE
    def eliminar(self, index):
        self.productos.pop(index)



# PRINCIPAL
# Interfaz de Streamlit
st.title("📊 Aplicación en Streamlit")

# Selección de página
st.sidebar.image("logo.png")
pagina = st.sidebar.selectbox("Selecciona una página:", ["🏠 Home", "📋 Ejercicio 1", "📋 Ejercicio 2", "📋 Ejercicio 3", "📋 Ejercicio 4"])

#Selección Home
if pagina == "🏠 Home":
    st.header("🏠 Bienvenido a la aplicación")
    # Información del estudiante
    st.markdown("### 👤 Información del Estudiante")
    st.write("**Nombre completo:** Ana Fernanda Rashel Fernandez Pamucena")
    st.write("**Módulo:** Python Fundamentals")
    st.write("**Año:** 2026")
    # Información general
    st.markdown("### 📌 Información General")
    st.write("""
    Soy estudiante titulada en Ingeniería Industrial con interés en el análisis de datos y automatización de procesos.
    Este proyecto forma parte del módulo de Python Fundamentals.
    """)
    # Descripción del proyecto
    st.markdown("### 📝 Descripción del Proyecto")
    st.write("""
    Este proyecto tiene como objetivo desarrollar una aplicación web interactiva utilizando Streamlit, para 
    visualizar datos, realizar análisis y presentar resultados de manera clara y dinámica.
    """)
    # Tecnologías utilizadas
    st.markdown("### 🛠️ Tecnologías Utilizadas")
    st.write("""
    - Python  
    - Streamlit  
    - Pandas  
    - Matplotlib  
    """)
    # Pie de página
    st.markdown("---")
    st.write("© 2026 - Proyecto Académico")

#Selección Ejercicio 1
elif pagina == "📋 Ejercicio 1":
    # Inicializar en sesión
    if "flujo" not in st.session_state:
        st.session_state.flujo = FlujoCaja()

    flujo = st.session_state.flujo

    # Interfaz
    st.title("💰 Flujo de caja con Listas")
    st.markdown("""
    Este módulo permite registrar ingresos y gastos en una lista.
    Podrás visualizar los movimientos y analizar el estado de tu flujo de caja.
    """)
    tabs = st.tabs(["👤 Entrada de datos", "📋 Mostrar datos"])
    
    with tabs[0]:
        # Entrada de datos
        st.subheader("➕ Agregar Movimiento")

        concepto = st.text_input("Concepto")
        tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")

        # Botón
        if st.button("Agregar movimiento", key="btn_movimiento"):
            if concepto and valor > 0:
                movimiento = Movimiento(concepto, tipo, valor)
                flujo.agregar_movimiento(movimiento)
                st.success("Movimiento agregado correctamente")
            else:
                st.error("Completa los datos correctamente. Concepto y Valor son campos obligatorios.")
        
    with tabs[1]:
        # Mostrar datos
        st.subheader("📋 Lista de Movimientos")

        if flujo.movimientos:
            df = flujo.obtener_dataframe()
            st.dataframe(df)

            # Resultados
            ingresos = flujo.total_ingresos()
            gastos = flujo.total_gastos()
            saldo = flujo.saldo()

            st.subheader("📊 Resumen")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Ingresos", f"S/ {ingresos:.2f}")
            col2.metric("Total Gastos", f"S/ {gastos:.2f}")
            col3.metric("Saldo Final", f"S/ {saldo:.2f}")

            # Estado
            st.subheader("📈 Estado del Flujo de Caja")

            if saldo > 0:
                st.success("✔ Flujo de caja a favor")
            elif saldo < 0:
                st.error("❌ Flujo de caja en contra")
            else:
                st.warning("⚖ Flujo equilibrado")

        else:
            st.info("No hay movimientos registrados")

#Selección Ejercicio 2
elif pagina == "📋 Ejercicio 2":
    # Inicializar en sesión
    if "registros" not in st.session_state:
        st.session_state.registros = RegistroVentas()

    registros = st.session_state.registros

    # Interfaz
    st.title("🛒 Registro con NumPy, arrays y DataFrame")
    st.markdown("""
    Este formulario permite registrar productos utilizando arreglos de NumPy.
    Cada registro se almacena en arrays y se muestra en una tabla actualizada automáticamente.
    """)
    tabs = st.tabs(["👤 Formulario", "📋 Mostrar DataFrame"])

    with tabs[0]:
        # Formulario
        st.subheader("➕ Ingresar Producto")

        nombre = st.text_input("Nombre del producto")
        categoria = st.selectbox("Categoría", ["Electrónica", "Ropa", "Alimentos", "Otros"])
        precio = st.number_input("Precio", min_value=0.0, format="%.2f")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)

        # Botón
        if st.button("Agregar registro", key="btn_registro"):
            if nombre and precio > 0 and cantidad > 0:
                registros.agregar_registro(nombre, categoria, precio, cantidad)
                st.success("Registro agregado correctamente")
            else:
                st.error("Completa correctamente los datos. Nombre del producto y Precio son campos obligatorios.")

    with tabs[1]:
        # Mostrar DataFrame
        st.subheader("📊 Tabla de Registros")

        df = registros.obtener_dataframe()

        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No hay registros aún")

#Selección Ejercicio 3
elif pagina == "📋 Ejercicio 3":
    # Inicializar en sesión
    if "gestor_roi" not in st.session_state:
        st.session_state.gestor_roi = GestorROI()

    gestor = st.session_state.gestor_roi

    # Interfaz
    st.title("📊 Función desde librería externa")

    st.markdown("""
    Este módulo permite calcular el **ROI (Return on Investment)** usando una función externa.

    Fórmula:
    ROI = (ganancia neta / inversión) * 100
    """)
    tabs = st.tabs(["👤 Inputs", "📋 Historial"])

    with tabs[0]:
        # Inputs
        st.subheader("📥 Ingresar datos")

        ganancia = st.number_input("Ganancia neta", min_value=0.0)
        inversion = st.number_input("Inversión", min_value=0.01)

        # Botón
        if st.button("Calcular ROI", key="btn_roi"):
            try:
                resultado = gestor.ejecutar_funcion(ganancia, inversion)
                st.success(f"ROI: {resultado['roi_pct']} %")
            except Exception as e:
                st.error(str(e))

    with tabs[1]:
        # Historial
        st.subheader("📊 Historial de Resultados")

        df = gestor.obtener_historial()

        if not df.empty:
            st.dataframe(df)
        else:
            st.info("Aún no hay cálculos realizados")


#Selección Ejercicio 4
elif pagina == "📋 Ejercicio 4":
    # Inicializar en sesión
    # Inicializar sesión
    if "gestor_inv" not in st.session_state:
        st.session_state.gestor_inv = GestorInventario()

    gestor = st.session_state.gestor_inv

    # Interfaz
    st.title("📦 Sistema de Inventario (CRUD)")

    st.markdown("""
    Aplicación para gestionar productos usando la clase **InventarioProducto**.
    Permite crear, visualizar, actualizar y eliminar registros.
    """)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Crear", "Leer", "Actualizar", "Eliminar"])

    # ---------------- CREAR ----------------
    with tab1:
        st.subheader("➕ Crear producto")

        with st.form("form_crear", clear_on_submit=True):

            nombre = st.text_input("Nombre")
            costo = st.number_input("Costo unitario", min_value=0.01)
            precio = st.number_input("Precio unitario", min_value=0.01)
            stock = st.number_input("Stock actual", min_value=0)
            stock_min = st.number_input("Stock mínimo", min_value=0)

            submitted = st.form_submit_button("Agregar producto")

            if submitted:
                if not nombre.strip():
                    st.error("El nombre es obligatorio. Intente registrar nuevamente")
                else:
                    try:
                        if any(p.nombre.lower() == nombre.lower() for p in gestor.productos):
                            st.error("Ya existe un producto con ese nombre, se recomienda actualizar la información del producto existente")
                        else:
                            gestor.crear(nombre, costo, precio, stock, stock_min)
                            st.toast("Producto agregado correctamente", icon="✅")

                    except Exception:
                        st.toast("Error al crear el producto", icon="❌")


    # ---------------- LEER ----------------
    with tab2:
        st.subheader("📋 Inventario")

        df = gestor.leer()
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No hay productos registrados")


    # ---------------- ACTUALIZAR ----------------
    with tab3:
        st.subheader("✏️ Actualizar producto")
        if "msg_ok" in st.session_state:
            st.success(st.session_state.msg_ok)
            del st.session_state.msg_ok

        if gestor.productos:

            # Mostrar nombres en vez de índices
            opciones = {i: p.nombre for i, p in enumerate(gestor.productos)}

            idx = st.selectbox(
                "Selecciona producto",
                options=list(opciones.keys()),
                format_func=lambda x: opciones[x],key="select_update"
            )

            producto = gestor.productos[idx]

            # FORM
            with st.form(key=f"form_update_{idx}"):

                nombre = st.text_input("Nombre", value=producto.nombre)
                costo = st.number_input("Costo", min_value=0.01, value=float(producto.costo_unitario))
                precio = st.number_input("Precio", min_value=0.01, value=float(producto.precio_unitario))
                stock = st.number_input("Stock", min_value=0, value=int(producto.stock_actual))
                stock_min = st.number_input("Stock mínimo", min_value=0, value=int(producto.stock_minimo))

                submitted = st.form_submit_button("Actualizar")

                if submitted:
                    try:
                        if not nombre.strip():
                            st.error("El nombre no puede estar vacío")
                        else:
                            gestor.actualizar(idx, nombre, costo, precio, stock, stock_min)
                            st.session_state.msg_ok = "Producto actualizado correctamente"
                            st.rerun()

                    except Exception as e:
                        st.error(str(e))

        else:
            st.info("No hay productos para actualizar")


    # ---------------- ELIMINAR ----------------
    with tab4:
        st.subheader("🗑️ Eliminar producto")
        if "msg_delete" in st.session_state:
            st.success(st.session_state.msg_delete)
            del st.session_state.msg_delete

        if gestor.productos:

            # 👉 Diccionario índice → nombre
            opciones = {i: p.nombre for i, p in enumerate(gestor.productos)}

            idx = st.selectbox(
                "Selecciona producto",
                options=list(opciones.keys()),
                format_func=lambda x: opciones[x],key="select_delete"
            )

            if st.button("Eliminar", key="btn_eliminar"):
                gestor.eliminar(idx)
                st.session_state.msg_delete = f"Producto {opciones[idx]} eliminado"
                st.rerun()

        else:
            st.info("No hay productos para eliminar")