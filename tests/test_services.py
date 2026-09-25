@pytest.mark.parametrize("dose", [0, -1, float("nan"), float("inf")])
def test_invalid_dose_is_rejected(dose):
    data = sample_data()
    with pytest.raises(ValueError):
        create_application(data, 1, 1, dose, "2026-09-23")
    assert data["fertilizers"][1].stock_ml == 100
    assert data["applications"] == []


def test_unknown_id_and_invalid_date_do_not_change_stock():
    data = sample_data()
    for plant_id, date_value in [(99, "2026-09-23"), (1, "2026-02-30")]:
        with pytest.raises(ValueError):
            create_application(data, plant_id, 1, 20, date_value)
    assert data["fertilizers"][1].stock_ml == 100


def test_names_are_checked_and_comma_is_accepted():
    data = sample_data()
    with pytest.raises(ValueError):
        add_plant(data, " роза ")
    with pytest.raises(ValueError):
        add_plant(data, "   ")
    assert positive_number("2,5") == 2.5
    for value in ["abc", "-0", "0", "NaN", "inf"]:
        with pytest.raises(ValueError):
            positive_number(value)


def test_objects_have_string_representation_and_methods():
    data = sample_data()
    plant = data["plants"][1]
    fertilizer = data["fertilizers"][1]
    assert "Роза" in str(plant)
    assert "остаток" in str(fertilizer)
    assert fertilizer.can_spend(50)
    assert not fertilizer.can_spend(150)
