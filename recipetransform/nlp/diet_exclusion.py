import recipetransform.tools.database as tools

meats = ["Beef Products", "Poultry Products", "Pork Products", "Sausages and Luncheon Meats"]
excluded_food_groups = {
	"Pescetarian" : meats,
	"Ovo vegetarian" : meats + ["Finfish and Shellfish Products"],
	"Lacto vegetarian" : meats + ["Finfish and Shellfish Products"],
	"Lacto-ovo vegetarian" : meats + ["Finfish and Shellfish Products"],
	"Vegan" :  meats + ["Finfish and Shellfish Products", "Dairy and Egg Products"]
}


db = tools.DBconnect()
db.exclusion_table.drop()
for group in excluded_food_groups:
	line = {"diet" : group, "excluded" : excluded_food_groups[group]}
	db.exclusion_table.insert(line)