#
# My first shell script
#
clear
echo "testing http://localhost:3333/listAgency ..."
python -mwebbrowser http://localhost:3333/listAgency

echo "testing http://localhost:3333/listRouteOf/ecu ..."
python -mwebbrowser http://localhost:3333/listRouteOf/ecu

echo "testing http://localhost:3333/routeConfig/ecu/507 ..."
python -mwebbrowser http://localhost:3333/routeConfig/ecu/507

echo "testing http://localhost:3333/predict/ecu/507/chrisgym"
python -mwebbrowser http://localhost:3333/predict/ecu/507/chrisgym

echo "testing show status of queries slower than 0.5 seconds http://localhost:3333/showStat/0.5"
python -mwebbrowser http://localhost:3333/showStat/0.5

echo "testing show status of queries slower than 0.3 seconds http://localhost:3333/showStat/0.3"
python -mwebbrowser http://localhost:3333/showStat/0.3