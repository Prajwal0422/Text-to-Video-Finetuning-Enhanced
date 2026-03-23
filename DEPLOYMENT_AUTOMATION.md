# Deployment Automation Guide

## Overview
This guide covers automated deployment strategies for NEXUS VISION video generation system.

## Deployment Methods

### 1. Docker Deployment

#### Build Image
```bash
docker build -t nexus-vision:latest .
```

#### Run Container
```bash
docker run -d \
  -p 8000:8000 \
  -e PEXELS_API_KEY=your_key_here \
  -v $(pwd)/outputs:/app/outputs \
  --name nexus-vision \
  nexus-vision:latest
```

#### Docker Compose
```yaml
version: '3.8'
services:
  nexus-vision:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PEXELS_API_KEY=${PEXELS_API_KEY}
    volumes:
      - ./outputs:/app/outputs
    restart: unless-stopped
```

### 2. Cloud Deployment

#### AWS EC2
1. Launch EC2 instance (t3.medium or larger)
2. Install dependencies
3. Clone repository
4. Configure environment
5. Start service with systemd

#### Google Cloud Run
```bash
gcloud run deploy nexus-vision \
  --image gcr.io/PROJECT_ID/nexus-vision \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances
```bash
az container create \
  --resource-group nexus-vision-rg \
  --name nexus-vision \
  --image nexusvision/nexus-vision:latest \
  --dns-name-label nexus-vision \
  --ports 8000
```

### 3. Kubernetes Deployment

#### Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus-vision
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nexus-vision
  template:
    metadata:
      labels:
        app: nexus-vision
    spec:
      containers:
      - name: nexus-vision
        image: nexusvision/nexus-vision:latest
        ports:
        - containerPort: 8000
        env:
        - name: PEXELS_API_KEY
          valueFrom:
            secretKeyRef:
              name: nexus-secrets
              key: pexels-api-key
```

## CI/CD Pipeline

### GitHub Actions
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t nexus-vision .
      
      - name: Push to registry
        run: |
          docker tag nexus-vision registry.example.com/nexus-vision
          docker push registry.example.com/nexus-vision
      
      - name: Deploy to production
        run: |
          ssh user@server 'docker pull registry.example.com/nexus-vision'
          ssh user@server 'docker-compose up -d'
```

## Monitoring

### Health Checks
- Endpoint: `/api/health`
- Frequency: Every 30 seconds
- Timeout: 5 seconds

### Metrics
- Generation success rate
- Average response time
- Queue length
- Error rate

### Alerts
- Service down
- High error rate (> 5%)
- Slow response time (> 60s)
- Queue backup (> 100 jobs)

## Scaling

### Horizontal Scaling
- Add more instances behind load balancer
- Use shared storage for outputs
- Implement distributed queue

### Vertical Scaling
- Increase CPU/RAM for faster processing
- Add GPU for potential future enhancements
- Optimize worker count

## Backup Strategy

### Automated Backups
- Daily backup of generated videos
- Weekly backup of metadata
- Monthly archive to cold storage

### Backup Script
```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)
tar -czf backup-$DATE.tar.gz outputs/
aws s3 cp backup-$DATE.tar.gz s3://nexus-backups/
```

## Security

### SSL/TLS
- Use Let's Encrypt for free certificates
- Configure nginx as reverse proxy
- Enable HTTPS redirect

### API Security
- Rate limiting enabled
- API key authentication
- CORS properly configured
- Security headers added

## Performance Optimization

### Caching
- Enable clip caching
- Use CDN for video delivery
- Implement Redis for session storage

### Database
- Use PostgreSQL for metadata
- Index frequently queried fields
- Regular vacuum and analyze

## Troubleshooting

### Common Issues
1. **Service won't start**: Check logs, verify dependencies
2. **Slow generation**: Check API key, network connectivity
3. **Out of disk space**: Clean old outputs, increase storage
4. **High memory usage**: Reduce worker count, optimize clips

### Log Locations
- Application logs: `/var/log/nexus-vision/app.log`
- Error logs: `/var/log/nexus-vision/error.log`
- Access logs: `/var/log/nginx/access.log`

## Maintenance

### Regular Tasks
- Weekly: Review logs, check disk space
- Monthly: Update dependencies, security patches
- Quarterly: Performance review, optimization

### Update Procedure
1. Backup current version
2. Pull latest code
3. Run tests
4. Deploy to staging
5. Verify functionality
6. Deploy to production
7. Monitor for issues

## Cost Optimization

### Tips
- Use spot instances for non-critical workloads
- Implement auto-scaling based on demand
- Archive old videos to cheaper storage
- Optimize video quality vs file size
- Use reserved instances for predictable load

## Support

### Resources
- Documentation: https://docs.nexusvision.com
- Support: support@nexusvision.com
- Community: https://community.nexusvision.com
- Status: https://status.nexusvision.com
