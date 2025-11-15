import streamlit as st
import pandas as pd

# ---------- Configuración de la página ----------
st.set_page_config(
    page_title="Catálogo Inmobiliario",
    page_icon="🏡",
    layout="wide"
)

LOGO_PATH = "logo_fbmr.jpg"  # cambia el nombre si tu logo se llama distinto

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

# ---------- Encabezado con logo ----------
with st.container():
    col_logo, col_titulo = st.columns([1, 3])
    with col_logo:
        # Si hay problema con la imagen, simplemente no se muestra
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

# ---------- Sidebar: filtros ----------
st.sidebar.header("Filtros de búsqueda")

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

st.sidebar.markdown("---")
st.sidebar.caption("Demo inmobiliaria • Streamlit")

# ---------- Filtro de datos ----------
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

# ---------- UI principal ----------
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
