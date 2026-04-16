# 🛡️ Secure EC2 Web Server — AWS Cloud Project

![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?style=flat&logo=amazonaws&logoColor=white)
![Nginx](https://img.shields.io/badge/Web_Server-Nginx-009639?style=flat&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/Automation-Boto3-3776AB?style=flat&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat)

---

## 📌 Overview

Deployed a production-style, security-hardened web server on AWS EC2 using Amazon Linux 2023 and Nginx.  
This project covers core cloud fundamentals: compute, networking, IAM, monitoring, alerting, and Python automation — all within the AWS Free Tier.

---

## 🏗️ Architecture

```
![Architecture](docs/architecture-diagram.png)

---

## ☁️ AWS Services Used

| Service | Purpose |
|---------|---------|
| Amazon EC2 (t2.micro) | Compute — hosts the web server |
| Amazon Linux 2023 | Operating system (free tier AMI) |
| Nginx | Web server serving custom HTML page |
| AWS IAM | Least-privilege user + EC2 instance role |
| Security Groups | Network-level firewall (SSH locked to My IP) |
| Amazon EBS | Encrypted root volume (8GB gp2) |
| CloudWatch Agent | Custom metrics — memory & disk usage |
| CloudWatch Alarms | CPU utilization alert (>70% threshold) |
| Amazon SNS | Email notification on alarm trigger |
| AWS Boto3 (Python) | Automation — instance state + alarm check |

---

## 🔒 Security Practices Applied

- **SSH access restricted to My IP only** — no public SSH exposure
- **EBS root volume encrypted at rest** — data protected at storage level
- **EC2 uses IAM Role** — zero hardcoded credentials on the instance
- **IAM user follows least-privilege** — only EC2 + CloudWatch permissions
- **Root AWS account not used** — dedicated IAM user for all operations
- **`.pem` key and credentials excluded from version control** via `.gitignore`

---

## 📁 Repository Structure

```
aws-ec2-secure-webserver/
├── check_ec2_status.py          # Boto3 automation script
├── cloudwatch-agent-config.json # CloudWatch Agent configuration
├── .gitignore                   # Excludes keys, credentials, cache
├── README.md                    # This file
├── Architecture-diagram.png     # draw.io architecture diagram
├── ss01-iam-user.png
├── ss03-ec2-running.png
├── ss04-security-group.png
├── ss05-ebs-encrypted.png
├── ss06-nginx-browser.png
├── ss08-cloudwatch-agent.png
├── ss10-cloudwatch-alarm.png
├── ss11-sns-confirmed.png
└── ss12-boto3-output.png
```

---

## 🚀 Setup & Deployment Steps

### Prerequisites
- AWS account (free tier)
- Ubuntu local machine with AWS CLI + Python 3 + Boto3 installed
- AWS IAM user credentials configured via `aws configure`

### 1 — IAM Setup
Create a least-privilege IAM user (`ec2-project-user`) with `AmazonEC2FullAccess` and `CloudWatchFullAccess`.  
Create an IAM Role (`ec2-cloudwatch-role`) with `CloudWatchAgentServerPolicy` for EC2 to use.

### 2 — Launch EC2
- AMI: Amazon Linux 2023 | Type: t2.micro | Region: ap-southeast-2
- Security Group: SSH (port 22, My IP only) + HTTP (port 80, public)
- EBS: 8GB gp2, encryption enabled
- Attach IAM Role: `ec2-cloudwatch-role`

### 3 — Connect & Configure Nginx
```bash
chmod 400 ~/.ssh/ec2-key.pem
ssh -i ~/.ssh/ec2-key.pem ec2-user@PUBLIC_IP

sudo dnf update -y
sudo dnf install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 4 — Install CloudWatch Agent
```bash
sudo dnf install amazon-cloudwatch-agent -y
# Deploy config file then start agent:
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```

### 5 — CloudWatch Alarm + SNS
- SNS: Create topic `ec2-cpu-alerts` → email subscription → confirm in inbox
- CloudWatch: Create alarm on `CPUUtilization > 70%` for 2 consecutive 5-min periods → notify SNS topic

### 6 — Run Boto3 Script (local machine)
```bash
python3 check_ec2_status.py
# Output: EC2 instance state + CloudWatch alarm state
```

---

## 📸 Screenshots

| Screenshot | Description |
|------------|-------------|
| ![](ss01-iam-user.png) | IAM user with least-privilege policies |
| ![](ss03-ec2-running.png) | EC2 instance in running state |
| ![](ss04-security-group.png) | Security group — SSH locked to My IP |
| ![](ss05-ebs-encrypted.png) | EBS volume encryption enabled |
| ![](ss06-nginx-browser.png) | Custom Nginx page live in browser |
| ![](ss08-cloudwatch-agent.png) | CloudWatch Agent active on EC2 |
| ![](ss10-cloudwatch-alarm.png) | CloudWatch CPU alarm configured |
| ![](ss11-sns-confirmed.png) | SNS email subscription confirmed |
| ![](ss12-boto3-output.png) | Boto3 script output in terminal |

---

## 💰 Cost

All resources operate within the **AWS Free Tier**.  
⚠️ Remember to **stop your EC2 instance** when not actively using it to avoid unexpected charges.

---

## 🧠 What I Learned

- How to launch and harden an EC2 instance from scratch
- IAM least-privilege design for both users and instance roles
- Difference between Security Groups (stateful) and network-level controls
- Installing and configuring the CloudWatch Agent for custom metrics
- Setting up SNS email alerts triggered by CloudWatch alarms
- Writing Boto3 Python scripts to query AWS resources programmatically
- Importance of never committing credentials or `.pem` keys to version control

---

## 👤 Author

**Gregory Suzan**  
6+ year graphic designer transitioning into cloud computing  
📍 Australia | ☁️ AWS | 🐍 Python  
[GitHub](https://github.com/GregorySuzan)
