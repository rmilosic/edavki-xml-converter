# Your Degiro-to-eDavki XML Builder

The Degiro-to-eDavki XML Converter is a tool designed to simplify the process of reporting paid out dividends from your Degiro trading platform to the Slovenian Tax reporting platform, eDavki. The tool streamlines the creation of an XML file, ensuring seamless integration with the eDavki system.


## Table of Contents

- [Main features](#main-features)
- [Limitations](#limitations)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Main Features

1. Account Statement Integration
The converter accepts your Degiro account extract in CSV format, allowing you to easily import your trading data for dividend reporting.

2. YAML Config Customization
Tailor the reporting process to your specific needs by providing custom data within a YAML configuration file. This flexibility ensures that the tool adapts to your unique financial circumstances.

3. Yearly Reporting
Choose the reporting year of interest, and the converter will generate an XML file containing the relevant dividend information for the specified period.

4. XML Output for eDavki
The tool generates a structured XML file ready for direct import into the eDavki Slovenian Tax reporting platform. This streamlines the reporting process, reducing the potential for errors and ensuring compliance. Make sure to do due diligence though.

## Limitations

1. Single Source Country
The Degiro-to-eDavki XML Converter currently supports reporting dividends from a single source country. It simplifies the reporting process by focusing on a single tax jurisdiction.

2. USD Currency Support
The tool is designed to handle dividends paid in USD. Future versions may extend support to additional currencies based on user demand and platform compatibility.

## Installation


```bash
# Clone the repository
git clone https://github.com/rmilosic/edavki-xml-converter.git

# Change into the project directory
cd your_project

# Install dependencies
pip install -r requirements.txt

```

## Usage
```bash
# Run the main script
python -m src.main Account.csv -y 2022 -c config_2022.yaml
```
* The tool is expecting the Degiro statement to be in data/ folder in CSV format
* You need to copy, modify and rename the config.example.yaml file within config/ folder and provide path to it under -c flag argument. Otherwise, program assumes it's named config.yaml
* Provide -y argument followed by the year you are doing the report for


## Contributing

If you'd like to contribute to the project, follow these steps:

1. Fork the project
2. Create your feature branch (git checkout -b feature/your-feature)
3. Commit your changes (git commit -m 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Open a pull request

## License

This project is licensed under the  MIT License - see the file LICENSE.md file for details.