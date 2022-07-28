from os import path
config = {

    # ChromeDriver
    "chromedriver_path": r'/usr/lib/chromium-browser/chromedriver',

    # Cache
    "cache_folder": r"./cache/cache.txt",

    # Firebase Certificate
    "certificate_path": path.join("home", "pi", "bin", "check-my-grades", "bot_creds.json"),

    # QIS 
    "qis_url": r"https://qisserver.htwk-leipzig.de/qisserver/rds?state=user&type=0",
    "qis_uname": "fzasada",
    "qis_pword": "4ZRpz7CR",

    # Email
    "email_credentials": {
        "mail_email": "xtract.fea@gmail.com",
        "mail_pword": r"iumixnesoznogdvr"
    },
    "mail_priv_email": "florian.zasada@gmail.com"

}