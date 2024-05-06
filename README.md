# WeatherStation

This repo will be used for our BTS project which consist of creating a weather station.  
For this project used a raspberry pi 3B and a TZ-BT04 wich is a basic bluetooth HR/Temp sensor.

## How does it work
<img src="./Schematics/howdoesitwork.svg">

## How to use

Clone the repo with this command :  
```git clone https://github.com/jeanGaston/WeatherStation.git```

Then go into the repo folder :  
```cd WeatherStation```

Make the Install script executable using this command :  
```chmod +x Install.sh```

Then execute it with sudo :  
```sudo ./Install.sh ```

Access the web interface in your browser at `http://localhost:5000`.

## Usage
- Navigate to `http://localhost:5000` to view sensor data and configure system settings.
- Check the logs for any errors or alerts.

## Contributing
Contributions are welcome! If you have any suggestions or improvements, please submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.