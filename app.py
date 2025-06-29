from datetime import datetime, date, timedelta
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Multi-Berth Port Ship Service Planner", layout="wide")

st.title("⚓ Multi-Berth Port Ship Service Planning System")
st.markdown("**Prepared by: Eng. Aseel Omar Ali Ahmed Qasem**")
st.markdown("Configure your port settings and ships in the sidebar, then click **'Calculate Schedule'** to generate the optimal berth assignments and timeline.")

with st.sidebar:
    st.header("🛠 Port Configuration")
    num_berths = st.number_input("Number of Berths", min_value=1, value=3)

    st.header("🚢 Ship Details")
    num_ships = st.number_input("Number of Ships", min_value=1, value=3)

    ships = []
    for i in range(int(num_ships)):
        st.subheader(f"Ship {i + 1}")
        name = st.text_input(f"Ship Name {i + 1}", value=f"Ship-{i + 1}", key=f"name_{i}")
        arrival_date = st.date_input(f"Arrival Date {i + 1}", key=f"date_{i}")
        service_duration = st.number_input(f"Service Duration (hrs) {i + 1}", min_value=1, value=2, key=f"duration_{i}")

        ships.append({
            "name": name,
            "arrival_date": arrival_date,
            "service_duration": service_duration
        })

if st.button("Calculate Schedule"):
    st.subheader("📋 Schedule Results")

    ships_sorted = sorted(ships, key=lambda x: x["arrival_date"])
    schedule = []
    berth_end_times = [datetime.combine(date.today(), datetime.min.time()) for _ in range(int(num_berths))]

    for ship in ships_sorted:
        ship_arrival = datetime.combine(ship["arrival_date"], datetime.min.time())
        assigned_berth = berth_end_times.index(min(berth_end_times))

        start_time = max(ship_arrival, berth_end_times[assigned_berth])
        end_time = start_time + timedelta(hours=ship["service_duration"])

        berth_end_times[assigned_berth] = end_time

        schedule.append({
            "Ship": ship["name"],
            "Berth": f"Berth {assigned_berth + 1}",
            "Start": start_time,
            "End": end_time
        })

    st.write("### 🗓 Final Schedule Table")
    st.dataframe([{
        "Ship": s["Ship"],
        "Berth": s["Berth"],
        "Start": s["Start"].strftime("%Y-%m-%d %H:%M"),
        "End": s["End"].strftime("%Y-%m-%d %H:%M")
    } for s in schedule])

    st.write("### 📊 Gantt Chart")
    fig = px.timeline(
        schedule,
        x_start="Start",
        x_end="End",
        y="Ship",
        color="Berth",
        title="Ship Service Timeline per Berth"
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)