import streamlit as st
from PIL import Image, UnidentifiedImageError
import numpy as np
from model import load_tf_segmentation_model, segment_rooftop
from area import calculate_rooftop_area, estimate_solar_capacity
from cost import estimate_roi
from summary import generate_summary
from llm import call_llm
import matplotlib.pyplot as plt

st.set_page_config(page_title='Solar Rooftop AI assistant', layout='centered')

st.title('☀️ Solar Rooftop AI Assistant')
st.write('Upload sattelite image to calculate solar potential')

upload_file = st.file_uploader('Choose a rooftop image',type=['jpg','jpeg','png'])
panel_power = st.number_input(
    label="Enter the wattage of one solar panel (W):",
    min_value=100,
    max_value=600,
    value=330,
    step=10
)

panel_area = st.number_input(
    label="Enter the area of one solar panel (sq. meters):",
    min_value=1.0,
    max_value=40.0,
    value=1.7,
    step=0.1,
    help="Typical panels are around 1.6–2.0 sq.m"
)


if upload_file is not None:
    try:
        img = Image.open(upload_file)
        st.image(img, caption='Upload rooftop image')
        st.success('Uploaded Succesfully')

        if st.button('Analyze rooftop'):
            st.info('Segmentation will run')
            with st.spinner("Loading Model and segmenting..."):
                model, extractor = load_tf_segmentation_model()
                mask = segment_rooftop(model, extractor, img)

            
                fig, ax = plt.subplots()
                ax.imshow(mask, cmap='nipy_spectral')
                ax.set_title("Predicted Segmentation Mask")
                st.pyplot(fig)
                

            rooftop_area = calculate_rooftop_area(mask)
            num_panels, estimated_kw = estimate_solar_capacity(rooftop_area, panel_power, panel_area)

            st.success(f"Estimated Rooftop Area: {rooftop_area:.2f} sq. meters")
            st.info(f"Estimated Panels: {num_panels}")
            st.info(f"Total Estimated Output: {estimated_kw} kW (with {panel_power}W panels of {panel_area} m² each)")
            st.session_state['rooftop_area'] = rooftop_area
            st.session_state['panel_power'] = panel_power
            st.session_state['num_panels'] = num_panels
            st.session_state['estimated_kw'] = estimated_kw
        
    except UnidentifiedImageError:
        st.error('Unexpected Image file')

    except Exception as e:
        st.error('An unexpected error occured')

        
    if 'estimated_kw' in st.session_state:
        st.header("🔧 ROI Estimation Settings")
        cost_per_watt = st.number_input(
            "Installation cost per watt (₹/W):",
            min_value=30.0, max_value=80.0, value=45.0, step=0.5
        )
        electricity_rate = st.number_input(
            "Electricity rate (₹ per kWh):",
            min_value=3.0, max_value=10.0, value=7.0, step=0.1
        )
        sunlight_hours = st.number_input(
            "Average sunlight hours per day:",
            min_value=2.0, max_value=8.0, value=5.5, step=0.1
        )

        roi_data = estimate_roi(
            st.session_state['estimated_kw'], cost_per_watt, electricity_rate, sunlight_hours
        )

        st.header("📈 ROI Estimate")
        st.info(f"💰 Installation Cost: ₹{roi_data['installation_cost']:,}")
        st.info(f"⚡ Estimated Annual Output: {roi_data['annual_output_kwh']} kWh")
        st.info(f"💸 Annual Savings: ₹{roi_data['annual_savings']:,}")
        
        if roi_data['payback_years']:
            st.success(f"⏳ Payback Period: {roi_data['payback_years']} years")
        else:
            st.warning("ROI cannot be calculated (check your inputs)")


    if all(k in st.session_state for k in ['rooftop_area', 'num_panels', 'panel_power', 'estimated_kw']):
        summary_prompt = generate_summary({
            "area": st.session_state['rooftop_area'],
            "panels": st.session_state['num_panels'],
            "panel_wattage": st.session_state['panel_power'],
            "system_kw": st.session_state['estimated_kw'],
            "installation_cost": roi_data['installation_cost'],
            "annual_output": roi_data['annual_output_kwh'],
            "annual_savings": roi_data['annual_savings'],
            "payback_years": roi_data['payback_years']
        })

        st.header("💬 AI Recommendation")
        
        recommendation_text = None
        if st.button("Generate Recommendation"):
            with st.spinner("Generating summary..."):
                result = call_llm(summary_prompt)
                st.success("Recommendation generated!")
                st.markdown(result)
                recommendation_text = result

        if recommendation_text:
            report_content = f"""
Solar Rooftop AI Assistant Report
---------------------------------

Estimated Rooftop Area: {st.session_state['rooftop_area']:.2f} sq. meters
Estimated Number of Panels: {st.session_state['num_panels']}
Panel Wattage: {st.session_state['panel_power']} W
Total Estimated Output: {st.session_state['estimated_kw']} kW

Installation Cost: ₹{roi_data['installation_cost']:,}
Estimated Annual Output: {roi_data['annual_output_kwh']} kWh
Annual Savings: ₹{roi_data['annual_savings']:,}
Payback Period: {roi_data['payback_years']} years

AI Recommendation:
{recommendation_text}
        """

            st.download_button(
                label="📥 Download Report",
                data=report_content,
                file_name='solar_rooftop_report.txt',
                mime='text/plain'
            )