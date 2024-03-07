


# Proxy Tool

Proxy Tool is a Python script that helps you retrieve, validate, and utilize proxies for web scraping or anonymous browsing.

## Features

- Retrieve proxies from online sources
- Validate proxies to ensure they are working
- Save validated proxies to a file for reuse
- Support for both HTTP and HTTPS proxies
- Rotating user agents to mimic different web browsers
- Advanced retry mechanism with exponential backoff for failed requests
- Support for SOCKS proxies

## Requirements

- Python 3.x
- Requests library

## Installation

1. Clone the repository:

```
git clone https://github.com/pyroalww/main.py
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Run the `proxy_tool.py` script:

```
python proxy_tool.py
```

2. Follow the prompts to retrieve, validate, and utilize proxies.

## Configuration

- Modify the `proxy_type` parameter in the `get_proxies` function to retrieve different types of proxies (e.g., HTTP, HTTPS, SOCKS).
- Customize the user agent list in the `rotate_user_agent` function to mimic different web browsers.
- Adjust the retry settings in the `make_request` function for advanced retry mechanism customization.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or features you'd like to see.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
