import re

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def run(client, **fields):
    form = {"chromatic-number": "3", "number-of-vertices": "20", "number-of-instances": "10",
            "coloring-method": "first-fit"}
    form.update({key.replace("_", "-"): str(value) for key, value in fields.items()})
    return client.post("/", data=form)


def ratio(response):
    return float(re.search(r"Average Competitive Ratio: ([\d.]+)", response.get_data(as_text=True)).group(1))


def test_form_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Chromatic number" in response.data


@pytest.mark.parametrize("method", ["first-fit", "cbip"])
def test_run_shows_ratio_and_inline_image(client, method):
    response = run(client, coloring_method=method)
    assert response.status_code == 200
    assert ratio(response) > 0
    assert b"data:image/png;base64," in response.data


def test_cbip_always_uses_k_2(client):
    response = run(client, coloring_method="cbip", chromatic_number=7)
    assert response.status_code == 200
    assert b"k = 2" in response.data


def test_large_graphs_are_not_drawn(client):
    response = run(client, number_of_vertices=400, number_of_instances=1)
    assert response.status_code == 200
    assert b"data:image/png" not in response.data
    assert b"aren't drawn" in response.data


@pytest.mark.parametrize("fields, message", [
    ({"chromatic_number": "x"}, b"must be a whole number"),
    ({"chromatic_number": 0}, b"between 1 and 10"),
    ({"number_of_vertices": 5000}, b"between 1 and 500"),
    ({"number_of_vertices": 500, "number_of_instances": 500}, b"at most 100,000"),
    ({"coloring_method": "greedy"}, b"Choose First Fit or CBIP"),
])
def test_bad_input_is_rejected_with_a_message(client, fields, message):
    response = run(client, **fields)
    assert response.status_code == 400
    assert message in response.data


def test_form_keeps_the_values_entered(client):
    response = run(client, number_of_vertices=0)
    assert b'value="0"' in response.data


def test_no_file_is_written(client, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    run(client)
    assert list(tmp_path.iterdir()) == []
