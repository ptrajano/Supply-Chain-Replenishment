# Supply Chain Replenishment Optimization System

## Overview
This project develops an advanced inventory management system that integrates:
- Statistical bootstrapping for lead time estimation
- Recurrent Neural Networks (RNN) for demand forecasting
- Dynamic inventory optimization algorithms

The system determines optimal replenishment timing and quantities to minimize stockouts while reducing excess inventory.

## Key Features
- 📈 Multi-stage lead time modeling (supplier→DC→store)
- 🤖 RNN-based demand prediction with temporal pattern recognition
- 📊 95th percentile safety stock calculation
- ⚙️ Automated purchase order generation
- 📉 Performance tracking with KPIs (lost sales, inventory turns)

## Methodology
1. **Data Generation**: Simulated 4 years of sales data
2. **Lead Time Modeling**: Normal distribution with ceiling constraints
3. **Demand Forecasting**: RNN with weekly/monthly seasonality
4. **Inventory Optimization**: Dynamic reorder point calculation

## Results
Achieved:
- <3% lost sales across product categories
- 5-day average inventory coverage
- 63.27h processing time for 100k SKUs (8-core system)

For complete implementation details and analysis, please refer to [README.pdf](README.pdf).

## Requirements
- Python 3.8+
- TensorFlow 2.x
- Pandas, NumPy
- Matplotlib for visualization

## Future Work
- Parameter optimization for edge cases
- Cloud-based scaling solutions
- Real-world validation studies

> **Note**: The full technical documentation including mathematical formulations and case studies is available in [README.pdf](README.pdf).

## Author
Pedro Trajano Ferreira  
pedro.trajano.ferreira@gmail.com  
09/04/2025
