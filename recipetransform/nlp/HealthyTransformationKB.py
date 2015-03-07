"""
Knowledge Base to do Transformation from/to Healthy
"""

#Non-essential High Cal (append any non-main high Cal ingredients found in the search)

nonEssentialHighCal = [""]

highCalBad = ["whole milk", "evaporated whole milk", "yogurt", "cheese", "mayonnaise", "whipping cream", "sour cream", "cream cheese", "cheese", "bacon", "sausage", "ground beef", "eggs", "chorizo", "margarine", "butter", "salad dressing" ]

lowCalSubs = {
	"whole milk": ["skim milk"],
	"evaporated whole milk": ["evaporated fat-free milk", "skim milk", "reduced-fat milk"],
	"yogurt": ["low calorie yogurt"],
	"mayonnaise": ["non-fat miracle whip", "light mayonnaise"],
	"whipping cream": ["imitation whipped cream"],
	"sour cream": ["plain low-fat yogurt"],
	"cream cheese": ["light cream cheese", "fat-free cream cheese"],
	"cheese": ["fat-free cheese"],
	"bacon": ["canadian bacon", "lean ham"],
	"sausage": ["lean ham"],
	"ground beef": ["extra-lean ground beef", "ground turkey"],
	"eggs": ["egg whites", "egg substitutes"],
	"chorizo": ["turkey sausage", "vegetarian sausage"],
	"margarine": ["light spread margarine", "diet margarine"],
	"butter": ["whipped butter"],
	"salad dressing": ["reduced-calorie salad dressing", "fat-free salad dressing", "lemon juice", "wine vinegar"]
}

lowCalKeywords = ["fat-free", "light", "reduced-calorie", "low-fat"]
highCalKeywords = ["whole"]
lowCalGood = ["quinoa", "peanut butter", "avovados", "nuts", "olive oil", "bananas"]


highSodium = ["bacon", "canned fruit", "salt", "broth", "buttermilk", "cheese", "canned vegetables"]
lowSodiumSub = {
	"bacon": ["turkey bacon"],
	"canned fruit": ["fresh fruit"],
	"salt": ["lemon juice", "salt free seasonings" ],
	"broth": ["reduced sodium broth"],
	"buttermilk": ["milk", "yogurt"],
	"cheese": ["low sodium cheese", "cream cheese", "ricotta cheese"],
	"canned vegetables": ["low-sodium canned vegetables", "fresh vegetables"]
}

# Look for "salted", "canned"
highSodiumKeywords= ["salted", "canned", "cured"]

lowSodiumKeywords= ["fresh", "low-sodium", "unsalted"]
