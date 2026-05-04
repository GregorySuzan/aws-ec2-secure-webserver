import boto3

# === CONFIG ===
REGION = "us-east-1"                                      # ← Changed to correct region
INSTANCE_ID = "i-0ed0e012d024c1fb9"                      # ← Your current Instance ID

ec2 = boto3.client("ec2", region_name=REGION)
cw = boto3.client("cloudwatch", region_name=REGION)

# Check EC2 instance state
response = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
print(f"✅ EC2 Instance State: {state}")

# Check CloudWatch alarm state
alarms = cw.describe_alarms(AlarmNames=["ec2-high-cpu-alarm"])
for alarm in alarms["MetricAlarms"]:
    print(f"🔔 Alarm: {alarm['AlarmName']} → State: {alarm['StateValue']}")
