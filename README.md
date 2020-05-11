<p align="center">
  <img src="https://raw.githubusercontent.com/StegSchreck/PP-Auxmoney-Parser/master/PP-Auxmoney-Parser.png" width="500px">
</p>

# PP-Auxmoney-Parser
This script parses the interests generated by the loans you invested in on the P2P platform Auxmoney.
This data can then be used to be imported as CSV to [Portfolio Performance](https://www.portfolio-performance.info/). This project was inspired by https://github.com/ChrisRBe/PP-P2P-Parser.

Note that this project is not affiliated with Auxmoney or Portfolio Performance.

## Preconditions
1. Make sure you have Python3, Firefox and Xvfb installed on your system. This project is designed to run on Linux.
1. Checkout the project
    `git clone https://github.com/StegSchreck/PP-Auxmoney-Parser.git && cd PP-Auxmoney-Parser`
1. Install the requirements with pip for Python3
    `pip3 install -r requirements.txt`
1. Install Geckodriver

      * Use your system's package manager (if it contains Geckodriver)
        * Arch Linux: `pacman -S geckodriver`
        * MacOS: `brew install geckodriver`
      * Or execute `sudo ./InstallGeckodriver.sh`.
        For this you will need to have tar and wget installed.

## Running the script
To start the parser run the following command:
```
python3 main.py -u <your_auxmoney_username> -p <your_secret_password>
```

Upon completion, the script will print the name and location of the export file containing the data.
You can start the import to Portfolio Performance using this file then.

## Call arguments / parameters
### Mandatory
`-u` / `--username`: username for Auxmoney login

`-p` / `--password`: password for Auxmoney login

### Optional
`--earliest`: earliest date of transactions to be considered in the ISO format (e.g. `2019-12-31` for 31st december 2019)

`--latest`: latest date of transactions to be considered in the ISO format (e.g. `2019-12-31` for 31st december 2019)

`-d` / `--destination`: destination folder for the resulting CSV file containing the parsed data

`-v` / `--verbose`: increase output verbosity

`-x` / `--show_browser`: show the browser doing his work (this might help for debugging)

`-h` / `--help`: Display the help, including all possible parameter options

## Trouble shooting
### Script aborts with `WebDriverException`
If you recently updated your Firefox, you might encounter the following exception during the login attempt of the parser:
```
selenium.common.exceptions.WebDriverException: Message: Expected [object Undefined] undefined to be a string
```

This can be fixed by installing the latest version of [Mozilla's Geckodriver](https://github.com/mozilla/geckodriver)
by running again the _Install Geckodriver_ command mentioned [above](#preconditions).

### Login attempt does not work
This can have multiple explanations.
One is, that you are using a password which starts or ends with a space character.
This script is currently not capable of dealing with that.
If your credentials have a space character in the middle though, it will work fine. 
