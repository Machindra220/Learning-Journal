import streamlit as st
import json
import os
import pandas as pd
from datetime import date, datetime
import time

# -----------------------------
# Config
# -----------------------------
NOTES_FILE = "data/notes.json"
RES_FILE = "data/resources.json"
SECTIONS = [
    "Daily Exercise",
    "Learning Skill",
    "YouTube Work",
    "LinkedIn Work",
    "Trading Learning/Work"
]

# -----------------------------
# Helpers
# -----------------------------
def ensure_ids_and_fields(items, item_type="note"):
    """Ensure each item has id and required fields."""
    for item in items:
        if "id" not in item:
            item["id"] = str(time.time())
        if item_type == "note":
            if "date" not in item:
                item["date"] = str(date.today())
            if "section" not in item:
                item["section"] = "General"
            if "note" not in item:
                item["note"] = ""
        elif item_type == "resource":
            if "date" not in item:
                item["date"] = str(date.today())
            if "section" not in item:
                item["section"] = "General"
            if "url" not in item:
                item["url"] = ""
            if "desc" not in item:
                item["desc"] = ""
    return items

def load_json(path, item_type="note"):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                return ensure_ids_and_fields(data, item_type)
        except json.JSONDecodeError:
            return []
    return []

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# Page: Add Notes
# -----------------------------
def page_add_notes():
    st.title("➕ Add Notes")
    notes = load_json(NOTES_FILE, item_type="note")

    d = st.date_input("Date", value=date.today())
    section = st.selectbox("Section", SECTIONS)
    note = st.text_area("Notes (Markdown supported)")

    if st.button("Save Note"):
        notes.append({
            "id": str(datetime.now().timestamp()),
            "date": str(d),
            "section": section,
            "note": note
        })
        save_json(NOTES_FILE, notes)
        st.success("Note saved!")

# -----------------------------
# Page: Show Notes
# -----------------------------
def page_show_notes():
    st.title("📒 Show Notes")
    notes = load_json(NOTES_FILE, item_type="note")

    if notes:
        df = pd.DataFrame(notes) 
        df["date"] = pd.to_datetime(df["date"], errors="coerce") 
        df = df.sort_values("date", ascending=False) # 🔑 latest first 
        grouped = df.groupby(df["date"].dt.strftime("%Y-%m-%d"))

        for d, group in sorted(grouped, key=lambda x: x[0], reverse=True): # 🔑 sort keys descending
            st.markdown(f"### {d}")
            for _, row in group.iterrows():
                col_text, col_edit, col_delete = st.columns([0.8, 0.1, 0.1])
                col_text.markdown(f"— **{row['section']}** - {row['note']}")

                # Edit button
                if col_edit.button("✏️", key="edit_"+row["id"]):
                    st.session_state["edit_note_id"] = row["id"]

                # Delete button
                if col_delete.button("🗑️", key="delete_"+row["id"]):
                    notes = [n for n in notes if n["id"] != row["id"]]
                    save_json(NOTES_FILE, notes)
                    st.success("Note deleted!")
                    st.experimental_rerun()

                # Show edit box if this note is being edited
                if st.session_state.get("edit_note_id") == row["id"]:
                    new_note = st.text_area("Edit Note", row["note"], key="edit_text_"+row["id"])
                    if st.button("💾 Save", key="save_edit_"+row["id"]):
                        for n in notes:
                            if n["id"] == row["id"]:
                                n["note"] = new_note
                        save_json(NOTES_FILE, notes)
                        st.success("Note updated!")
                        st.session_state["edit_note_id"] = None
                        st.experimental_rerun()
    else:
        st.info("No notes yet.")


# -----------------------------
# Page: Add Resources
# -----------------------------
def page_add_resources():
    st.title("➕ Add Resources")
    resources = load_json(RES_FILE, item_type="resource")

    section = st.selectbox("Section", SECTIONS)
    url = st.text_input("Resource URL")
    desc = st.text_area("Description")

    if st.button("Add Resource"):
        resources.append({
            "id": str(datetime.now().timestamp()),
            "date": str(date.today()),
            "section": section,
            "url": url,
            "desc": desc
        })
        save_json(RES_FILE, resources)
        st.success("Resource added!")

# -----------------------------
# Page: Show Resources
# -----------------------------
def page_show_resources():
    st.title("🔗 Show Resources")
    resources = load_json(RES_FILE, item_type="resource")

    if resources:
        for r in resources[::-1]:
            col_text, col_edit, col_delete = st.columns([0.8, 0.1, 0.1])
            col_text.markdown(f"**{r['date']}** — **{r['section']}**: [{r['url']}]({r['url']}) — {r['desc']}")

            # Edit button
            if col_edit.button("✏️", key="edit_res_"+r["id"]):
                st.session_state["edit_res_id"] = r["id"]

            # Delete button
            if col_delete.button("🗑️", key="delete_res_"+r["id"]):
                resources = [x for x in resources if x["id"] != r["id"]]
                save_json(RES_FILE, resources)
                st.success("Resource deleted!")
                st.experimental_rerun()

            # Show edit box if this resource is being edited
            if st.session_state.get("edit_res_id") == r["id"]:
                new_desc = st.text_area("Edit Description", r["desc"], key="edit_desc_"+r["id"])
                if st.button("💾 Save", key="save_res_"+r["id"]):
                    for res in resources:
                        if res["id"] == r["id"]:
                            res["desc"] = new_desc
                    save_json(RES_FILE, resources)
                    st.success("Resource updated!")
                    st.session_state["edit_res_id"] = None
                    st.experimental_rerun()
    else:
        st.info("No resources yet.")


# -----------------------------
# Page: Calendar
# -----------------------------
def page_calendar():
    st.title("📆 Calendar View")
    notes = load_json(NOTES_FILE, item_type="note")
    resources = load_json(RES_FILE, item_type="resource")

    if notes or resources:
        df_notes = pd.DataFrame(notes)
        df_notes["date"] = pd.to_datetime(df_notes["date"], errors="coerce")

        df_res = pd.DataFrame(resources)
        df_res["date"] = pd.to_datetime(df_res["date"], errors="coerce")

        start_date = min(
            [df_notes["date"].min(), df_res["date"].min()]
        ).date() if not df_notes.empty or not df_res.empty else date.today()
        end_date = date.today()

        all_days = pd.date_range(start=start_date, end=end_date)

        summary_notes = df_notes.groupby("date").size().reset_index(name="notes_count")
        resource_days = set(df_res["date"].dt.date) if not df_res.empty else set()

        data = []
        for d in all_days:
            match = summary_notes[summary_notes["date"] == d]
            count = int(match["notes_count"].values[0]) if not match.empty else 0
            status = "✅" if count > 0 else ""
            res_mark = "🔵" if d.date() in resource_days else ""   # 🔑 blue mark
            data.append({
                "Date": d.strftime("%Y-%m-%d"),
                "Notes Count": count,
                "Notes Status": status,
                "Resource Status": res_mark
            })

        df_calendar = pd.DataFrame(data)
        df_calendar = df_calendar.sort_values("Date", ascending=False)  # 🔑 latest first
        st.dataframe(df_calendar)
    else:
        st.info("No notes or resources yet.")


# -----------------------------
# Page: Schedule
# -----------------------------
def page_schedule():
    st.title("📋 Schedule")

    import pandas as pd

    # -----------------------------
    # Daily schedule data
    # -----------------------------
    daily_schedules = [
        {
            "Time": "07:00 AM",
            "Standard": "Health Standard",
            "Notes": "30 mins walking or light exercise. Success = Just showing up."
        },
        {
            "Time": "08:00 AM",
            "Standard": "Skill Building Standard",
            "Notes": "30 mins active learning/practice. Success = 30 mins of focused study."
        },
        {
            "Time": "06:00 PM",
            "Standard": "YouTube Standard",
            "Notes": "30 mins planning or recording. Success = Software/Doc is open."
        },
        {
            "Time": "06:30 PM",
            "Standard": "LinkedIn Standard",
            "Notes": "20 mins engagement or drafting. Success = 100 words written."
        },
    ]
    df_daily = pd.DataFrame(daily_schedules)

    st.subheader("Daily Schedule")
    st.table(df_daily)

    # -----------------------------
    # Weekly schedule data
    # -----------------------------
    weekly_schedules = [
        {
            "Date": "Saturday every Week",
            "Standard": "Track Learning Streaks",
            "Notes": "30 mins Track Learning Streaks."
        }
    ]
    df_weekly = pd.DataFrame(weekly_schedules)

    st.subheader("Weekly Schedule")
    st.table(df_weekly)

    # -----------------------------
    # Monthly schedule data
    # -----------------------------
    monthly_schedules = [
        {
            "Date": "28th of every month",
            "Standard": "Finance Standard",
            "Notes": "30 mins finance tracking on sheet."
        }
    ]
    df_monthly = pd.DataFrame(monthly_schedules)

    st.subheader("Monthly Schedule")
    st.table(df_monthly)

# -----------------------------
# Main App
# -----------------------------
def main():
    st.sidebar.title("Learning Journal")

    page = st.sidebar.radio("Navigate", [
        "➕ Add Notes",
        "📒 Show Notes",
        "➕ Add Resources",
        "🔗 Show Resources",
        "📆 Calendar",
        "📋 Schedule"
    ])

    if page == "➕ Add Notes":
        page_add_notes()
    elif page == "📒 Show Notes":
        page_show_notes()
    elif page == "➕ Add Resources":
        page_add_resources()
    elif page == "🔗 Show Resources":
        page_show_resources()
    elif page == "📆 Calendar":
        page_calendar()
    elif page == "📋 Schedule":
        page_schedule()


if __name__ == "__main__":
    main()
