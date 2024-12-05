import matplotlib.pyplot as plt
import io
import base64


def generate_chart(chart_data, chart_type="bar"):
    fig, ax = plt.subplots()

    if chart_type == "bar":
        ax.bar(chart_data.keys(), chart_data.values())
    elif chart_type == "pie":
        ax.pie(chart_data.values(), labels=chart_data.keys(), autopct="%1.1f%%")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    plt.close(fig)

    return f"data:image/png;base64,{image_base64}"
