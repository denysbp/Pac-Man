from .db import DATA_BASE

if __name__ == "__main__":
    db = DATA_BASE()

    db.create_table()
    db.insert_on_table("Luis", 500)
    db.insert_on_table("Denys", 10000)
    db.insert_on_table("Carlos", 850)
    db.insert_on_table("Miguel", 1200)
    db.insert_on_table("Joao", 300)
    db.insert_on_table("Pedro", 1750)
    db.insert_on_table("Rafael", 950)
    db.insert_on_table("Bruno", 620)
    db.insert_on_table("Andre", 1100)
    db.insert_on_table("Tiago", 1450)
    db.insert_on_table("Eu", 1950)
    db.insert_on_table("E", 8)
    db.insert_on_table("ANA", 150)
    print(db.get_scores())
