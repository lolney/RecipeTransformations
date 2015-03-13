meats = ["Beef Products", "Poultry Products", "Pork Products", "Sausages and Luncheon Meats"]
excluded_food_groups = {
	"Pescetarian" : meats,
	"Vegetarian" : meats + ["Finfish and Shellfish Products"],
	"Vegetarian" : meats + ["Finfish and Shellfish Products"],
	"Vegetarian" : meats + ["Finfish and Shellfish Products"],
	"Vegan" :  meats + ["Finfish and Shellfish Products", "Dairy and Egg Products"]
}


for diet in excluded_food_groups:
	
