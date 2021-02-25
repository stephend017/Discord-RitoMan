from sqlalchemy import inspect

from discord_ritoman.db.session import config_name, postgresql_engine


def test_correct_config_used():
    """
    Tests that the correct database configuration object is being used
    """
    assert config_name == "TestingConfig"


def test_all_schemas_created():
    """
    Tests that all the defined schemas in the database are created
    successfully
    """
    inspector = inspect(postgresql_engine)
    schemas = inspector.get_schema_names()

    assert "public" in schemas

    for schema in schemas:
        if schema != "public":
            # this is not the schema we defined (other db stuff)
            continue
        assert len(inspector.get_table_names(schema=schema)) == 3
