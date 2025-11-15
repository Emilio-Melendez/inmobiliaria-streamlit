import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# ---------- Configuración de la página ----------
st.set_page_config(
    page_title="Catálogo Inmobiliario",
    page_icon="🏡",
    layout="wide"
)

LOGO_PATH = "logo_fbmr.jpg"  # cambia si tu archivo se llama distinto

# ---------- Datos de ejemplo ----------
@st.cache_data
def cargar_propiedades():
    data = [
        {
            "id": 1,
            "titulo": "Casa en Hacienda Real",
            "descripcion": "Casa cómoda ideal para familia pequeña.",
            "precio": 520000,
            "ciudad": "Ciénega de Flores",
            "colonia": "Hacienda Real 2do Sector",
            "tipo": "Casa",
            "estatus": "Disponible",
            "creditos": "Contado, Infonavit, crédito bancario",
            "m2_terreno": 52,
            "m2_construccion": 49
        },
        {
            "id": 2,
            "titulo": "Terreno en Fracc. Campestre",
            "descripcion": "Terreno para inversión a mediano plazo.",
            "precio": 350000,
            "ciudad": "General Zuazua",
            "colonia": "Campestre",
            "tipo": "Terreno",
            "estatus": "Disponible",
            "creditos": "Contado",
            "m2_terreno": 120,
            "m2_construccion": 0
        },
        {
            "id": 3,
            "titulo": "Casa céntrica",
            "descripcion": "Cerca de escuelas y comercios.",
            "precio": 890000,
            "ciudad": "Monterrey",
            "colonia": "Centro",
            "tipo": "Casa",
            "estatus": "Vendida",
            "creditos": "Contado, crédito bancario",
            "m2_terreno": 70,
            "m2_construccion": 90
        },
    ]
    return pd.DataFrame(data)

df = cargar_propiedades()

# ---------- Función para guardar contactos ----------
def guardar_contacto(nombre, telefono, correo, tipo_busqueda, presupuesto_min, presupuesto_max, mensaje):
    ruta = Path("contactos.csv")
    nuevo = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre": nombre,
        "telefono": telefono,
        "correo": correo,
        "tipo_busqueda": tipo_busqueda,
        "presupuesto_min": presupuesto_min,
        "presupuesto_max": presupuesto_max,
        "mensaje": mensaje
    }])

    try:
        if ruta.exists():
            existente = pd.read_csv(ruta)
            df_final = pd.concat([existente, nuevo], ignore_index=True)
        else:
            df_final = nuevo

        df_final.to_csv(ruta, index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        st.error(f"Ocurrió un error al guardar el contacto: {e}")
        return False

# ---------- Sidebar: navegación + filtros ----------
st.sidebar.image(LOGO_PATH, use_container_width=True)
st.sidebar.title("Menú")

pagina = st.sidebar.radio(
    "Ir a:",
    ["Catálogo", "Contacto"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Demo inmobiliaria • Streamlit")

# =====================================================
# ================== PÁGINA: CATÁLOGO =================
# =====================================================
if pagina == "Catálogo":
    # Encabezado
    with st.container():
        col_logo, col_titulo = st.columns([1, 3])
        with col_logo:
            try:
                st.image(LOGO_PATH, use_container_width=True)
            except Exception:
                st.write("")
        with col_titulo:
            st.title("Catálogo Inmobiliario")
            st.markdown(
                "Aplicación demo para mostrar propiedades, "
                "construida en **Python + Streamlit**."
            )

    st.markdown("---")

    # Filtros (en el sidebar, pero dependen del catálogo)
    st.sidebar.subheader("Filtros de búsqueda")

    precio_min = int(df["precio"].min())
    precio_max = int(df["precio"].max())

    rango_precios = st.sidebar.slider(
        "Rango de precio",
        min_value=precio_min,
        max_value=precio_max,
        value=(precio_min, precio_max),
        step=10000
    )

    ciudades = ["Todos"] + sorted(df["ciudad"].unique().tolist())
    ciudad_sel = st.sidebar.selectbox("Ciudad", ciudades)

    tipos = ["Todos"] + sorted(df["tipo"].unique().tolist())
    tipo_sel = st.sidebar.selectbox("Tipo de inmueble", tipos)

    estatuses = ["Todos"] + sorted(df["estatus"].unique().tolist())
    estatus_sel = st.sidebar.selectbox("Estatus", estatuses)

    # Filtro de datos
    filtro = (
        (df["precio"] >= rango_precios[0]) &
        (df["precio"] <= rango_precios[1])
    )

    if ciudad_sel != "Todos":
        filtro &= df["ciudad"] == ciudad_sel

    if tipo_sel != "Todos":
        filtro &= df["tipo"] == tipo_sel

    if estatus_sel != "Todos":
        filtro &= df["estatus"] == estatus_sel

    df_filtrado = df[filtro]

    # UI principal catálogo
    st.subheader(f"Propiedades encontradas: {len(df_filtrado)}")

    for _, row in df_filtrado.iterrows():
        with st.container(border=True):
            cols = st.columns([3, 1.5])
            with cols[0]:
                st.markdown(f"### {row['titulo']}")
                st.caption(f"{row['ciudad']} · {row['colonia']}")
                st.write(row["descripcion"])
                st.markdown(
                    f"**Créditos aceptados:** {row['creditos']}"
                )
                st.markdown(
                    f"**Terreno:** {row['m2_terreno']} m² · "
                    f"**Construcción:** {row['m2_construccion']} m²"
                )
            with cols[1]:
                st.metric("Precio", f"${row['precio']:,.0f}")
                st.markdown(f"**Tipo:** {row['tipo']}")
                estatus_badge = (
                    f"✅ {row['estatus']}" if row["estatus"] == "Disponible"
                    else f"⛔ {row['estatus']}"
                )
                st.markdown(f"**Estatus:** {estatus_badge}")
                st.button(
                    "Solicitar información",
                    key=f"btn_{row['id']}"
                )

    st.divider()
    with st.expander("Ver tabla completa"):
        st.dataframe(df, use_container_width=True)

# =====================================================
# ================== PÁGINA: CONTACTO =================
# =====================================================
elif pagina == "Contacto":
    with st.container():
        col_logo, col_titulo = st.columns([1, 3])
        with col_logo:
            try:
                st.image(LOGO_PATH, use_container_width=True)
            except Exception:
                st.write("")
        with col_titulo:
            st.title("Contacto")
            st.markdown(
                "Déjanos tus datos y lo que buscas, y un asesor te contactará "
                "para ayudarte a encontrar la mejor opción."
            )

    st.markdown("---")

    st.subheader("Formulario de contacto")

    with st.form("form_contacto"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo *")
            telefono = st.text_input("Teléfono / WhatsApp *")
            correo = st.text_input("Correo electrónico")
        with col2:
            tipo_busqueda = st.selectbox(
                "¿Qué tipo de propiedad buscas?",
                ["Casa", "Terreno", "Departamento", "Local comercial", "Otra"]
            )
            presupuesto_min, presupuesto_max = st.slider(
                "Rango de presupuesto aproximado",
                min_value=200000,
                max_value=2000000,
                value=(400000, 900000),
                step=50000
            )

        mensaje = st.text_area(
            "Cuéntanos más (colonia, ciudad, número de recámaras, etc.)",
            height=120
        )

        enviado = st.form_submit_button("Enviar solicitud")

        if enviado:
            if not nombre.strip() or not telefono.strip():
                st.error("Por favor, llena al menos tu nombre y teléfono.")
            else:
                ok = guardar_contacto(
                    nombre=nombre.strip(),
                    telefono=telefono.strip(),
                    correo=correo.strip(),
                    tipo_busqueda=tipo_busqueda,
                    presupuesto_min=presupuesto_min,
                    presupuesto_max=presupuesto_max,
                    mensaje=mensaje.strip()
                )
                if ok:
                    st.success("✅ ¡Tu solicitud ha sido enviada! Un asesor se pondrá en contacto contigo.")
                    st.info(
                        "Esta es una demo: los datos se guardan en un archivo "
                        "`contactos.csv` dentro del proyecto."
                    )

    st.markdown("---")
    with st.expander("Solo admin: ver últimos registros (demo)"):
        ruta = Path("contactos.csv")
        if ruta.exists():
            contactos_df = pd.read_csv(ruta)
            st.dataframe(contactos_df.tail(10), use_container_width=True)
        else:
            st.caption("Aún no hay contactos registrados.")
