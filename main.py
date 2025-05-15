from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# List of common currency codes (can be expanded)
CURRENCIES = {
    "USD": {"name": "United States Dollar", "symbol": "$"},
    "EUR": {"name": "Euro", "symbol": "€"},
    "GBP": {"name": "British Pound Sterling", "symbol": "£"},
    "INR": {"name": "Indian Rupee", "symbol": "₹"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥"},
    "CAD": {"name": "Canadian Dollar", "symbol": "CA$"},
    "AUD": {"name": "Australian Dollar", "symbol": "A$"},
    "CHF": {"name": "Swiss Franc", "symbol": "CHF"},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥"},
    "HKD": {"name": "Hong Kong Dollar", "symbol": "HK$"},
    "SGD": {"name": "Singapore Dollar", "symbol": "S$"},
    "NZD": {"name": "New Zealand Dollar", "symbol": "NZ$"},
    "SEK": {"name": "Swedish Krona", "symbol": "kr"},
    "NOK": {"name": "Norwegian Krone", "symbol": "kr"},
    "DKK": {"name": "Danish Krone", "symbol": "kr"},
    "MXN": {"name": "Mexican Peso", "symbol": "$"},
    "ZAR": {"name": "South African Rand", "symbol": "R"},
    "RUB": {"name": "Russian Ruble", "symbol": "₽"},
    "BRL": {"name": "Brazilian Real", "symbol": "R$"},
    "TRY": {"name": "Turkish Lira", "symbol": "₺"},
    "PLN": {"name": "Polish Zloty", "symbol": "zł"},
    "THB": {"name": "Thai Baht", "symbol": "฿"},
    "MYR": {"name": "Malaysian Ringgit", "symbol": "RM"},
    "IDR": {"name": "Indonesian Rupiah", "symbol": "Rp"},
    "PHP": {"name": "Philippine Peso", "symbol": "₱"},
    "KRW": {"name": "South Korean Won", "symbol": "₩"},
    "AED": {"name": "UAE Dirham", "symbol": "د.إ"},
    "SAR": {"name": "Saudi Riyal", "symbol": "﷼"},
    "EGP": {"name": "Egyptian Pound", "symbol": "E£"},
    "NGN": {"name": "Nigerian Naira", "symbol": "₦"},
    "PKR": {"name": "Pakistani Rupee", "symbol": "₨"},
    "BDT": {"name": "Bangladeshi Taka", "symbol": "৳"},
}


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            base = request.form['base'].upper()
            target = request.form['target'].upper()

            if base == target:
                result = f"{amount} {base} = {amount} {target}"
            else:
                url = f"https://api.frankfurter.app/latest?amount={amount}&from={base}&to={target}"
                response = requests.get(url)
                data = response.json()

                if 'rates' in data and target in data['rates']:
                    converted = data['rates'][target]
                    result = f"{amount} {base} = {converted:.2f} {target}"
                else:
                    error = "Currency code not supported."
        except Exception:
            error = "Error processing your request."

    return render_template('index.html', result=result, error=error, currencies=CURRENCIES)


if __name__ == '__main__':
    app.run(debug=True)
