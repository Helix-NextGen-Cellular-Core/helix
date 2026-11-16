kubectl autoscale -n omec deployment amf --cpu-percent=50 --min=1 --max=20
kubectl autoscale -n omec deployment smf --cpu-percent=50 --min=1 --max=20
kubectl autoscale -n omec deployment udm --cpu-percent=50 --min=1 --max=20
kubectl autoscale -n omec deployment udr --cpu-percent=50 --min=1 --max=20