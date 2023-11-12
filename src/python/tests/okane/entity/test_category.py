from okane.entity.category import Category


def test_default_values():
    category = Category('Test')
    assert category.id == -1
    assert category.name == 'Test'
    assert category.parent is None


def test_custom_values():
    parent_category = Category('Parent')
    category = Category('Test', 1, parent_category)
    assert category.id == 1
    assert category.name == 'Test'
    assert category.parent == parent_category


def test_update_properties():
    category = Category('Test')
    category.id = 2
    category.name = 'Updated'
    category.parent = Category('Parent')
    assert category.id == 2
    assert category.name == 'Updated'
    assert category.parent is not None
