from flask import Flask, render_template, abort, request
import pandas as pd

app = Flask(__name__)
EXCEL_FILE = "storage_data.xlsx"

@app.route("/box/<int:row_id>")
def box_info(row_id):
    df = pd.read_excel(EXCEL_FILE)
    if row_id <= 0 or row_id > len(df):
        abort(404)
    data = df.iloc[row_id - 1].to_dict()
    return render_template("box.html", row=row_id, box=data)

@app.route("/", methods=["GET"])
def search():
    query = request.args.get("q", "").strip().lower()
    df = pd.read_excel(EXCEL_FILE)
    results = []

    if query:
        for i, row in df.iterrows():
            if query in str(row["Box Name"]).lower() or query in str(row["Contents"]).lower():
                results.append({"row": i + 1, "Box Name": row["Box Name"], "Contents": row["Contents"]})

    return render_template("search.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)