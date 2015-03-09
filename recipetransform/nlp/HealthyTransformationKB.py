"""
Knowledge Base to do Transformation from/to Healthy
"""

#Non-essential High Cal (append any non-main high Cal ingredients found in the search)

nonEssentialHighCal = [""]

highCalBad = ["whole milk", "evaporated whole milk", "yogurt", "cheese", "mayonnaise", "whipping cream", "sour cream", "cream cheese", "cheese", "bacon", "sausage", "ground beef", "eggs", "chorizo", "margarine", "butter", "salad dressing" ]

lowCalSubs = {
	"whole milk": [{"name": "milk",
					"descriptor": "skim"}],
	"evaporated whole milk": [{"name": "milk",
				"descriptor": "evaporated, fat-free"}, 
				{"name":"milk",
				"descriptor": "skim"}, 
				{"name": "milk",
				"descriptor": "reduced-fat"}],
	"yogurt": [{"name": "yogurt",
		    "descriptor": "low calorie"}],
	"mayonnaise": [{"name": "miracle whip",
			"descriptor": "non-fat"},
			{"name": "mayonnaise",
			"descriptor": "light"}],
	"whipping cream": [{"name": "cream",
			    "descriptor": "imitation whipped"}],
	"sour cream": [{"name": "yogurt",
					"descriptor": "plain low-fat"}],
	"cream cheese": [{"name": "cream cheese",
			"descriptor": "light"},
			{"name": "cream cheese",
			"descriptor": "fat-free"}],
	"cheese": [{"name": "cheese",
				"descriptor": "fat-free"}],
	"bacon": [{"name":"bacon",
				"descriptor": "canadian"},
				{"name": "ham",
				"descriptor": "lean"}],
	"sausage": [{"name": "ham",
				"descriptor": "lean"}],
	"ground beef": [{"name":"beef",
					"descriptor": "extra lean ground"},
					{"name": "turkey",
					"descriptor": "ground"}],
	"eggs": [{"name":"egg whites",
				"descriptor": ""},
				{"name": "egg substitutes",
				"descriptor": ""}],
	"chorizo": [{"name":"sausage",
				"descriptor": "turkey"},
				{"name": "sausage",
				"descriptor": "vegetarian"}],
	"margarine": [{"name": "margarine",
			"descriptor": "light spread"}],
	"butter": [{"name": "butter",
				"descriptor": "whipped"}],
	"salad dressing": [{"name": "salad dressing",
						"descriptor": "reduced-calorie"},
						{"name": "salad dressing",
						"descriptor": "fat-free"},
						{"name": "lemon juice",
						"descriptor": ""},
						{"name": "vinegar",
						"descriptor": "wine"}],
}

lowCalKeywords = ["fat-free", "light", "reduced-calorie", "low-fat"]
highCalKeywords = ["whole"]
lowCalGood = ["quinoa", "peanut butter", "avovados", "nuts", "olive oil", "bananas"]


highSodium = ["bacon", "canned fruit", "salt", "broth", "buttermilk", "cheese", "canned vegetables"]
lowSodiumSub = {
	"bacon": [{"name":"bacon",
				"descriptor": "turkey"}],
	"canned fruit": [{"name": "fruit",
					"descriptor": "fresh"}],
	"salt": [{"name": "lemon juice",
			"descriptor": ""},
			{"name": "seasonings",
			"descriptor": "salt free"}],
	"broth": [{"name":"broth",
			"descriptor": "reduced sodium"}],
	"buttermilk": [{"name": "milk",
				"descriptor": ""},
				{"name": "yogurt",
				"descriptor": ""}],
	"cheese": [{"name": "cheese",
				"descriptor": "low sodium"},
				{"name": "cream cheese",
				"descriptor": ""},
				{"name": "ricotta cheese",
				"descriptor": ""}],
	"canned vegetables": [{"name": "vegatables",
							"descriptor": "low sodium canned"}]
}

# Look for "salted", "canned"
highSodiumKeywords= ["salted", "canned", "cured"]

lowSodiumKeywords= ["fresh", "low-sodium", "unsalted"]