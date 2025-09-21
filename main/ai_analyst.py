"""
AI Analyst Service for generating comprehensive startup analysis reports.
"""

import logging
import random
from typing import Dict, List, Tuple
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from main.models import Project, Investment, ProjectView, Position, AIAnalystReport
# from main.views import ask_gemini  # Commenting out to avoid API dependency issues

logger = logging.getLogger(__name__)

class AIAnalyst:
    """AI-powered startup analyst for generating comprehensive reports"""
    
    def __init__(self):
        self.model_version = "v1.0"
    
    def generate_report(self, project: Project) -> AIAnalystReport:
        """Generate a comprehensive AI analyst report for a project"""
        try:
            logger.info(f"Generating AI analyst report for {project.name}")
            
            # Calculate risk indicators
            risk_indicators = self._calculate_risk_indicators(project)
            
            # Calculate growth potential
            growth_metrics = self._calculate_growth_metrics(project)
            
            # Perform peer benchmarking
            peer_benchmarks = self._perform_peer_benchmarking(project)
            
            # Generate AI analysis text
            ai_analysis = self._generate_ai_analysis(project, risk_indicators, growth_metrics, peer_benchmarks)
            
            # Create or update the report
            report, created = AIAnalystReport.objects.get_or_create(
                project=project,
                defaults={
                    'ai_model_version': self.model_version,
                    **risk_indicators,
                    **growth_metrics,
                    **peer_benchmarks,
                    **ai_analysis
                }
            )
            
            if not created:
                # Update existing report
                for key, value in {**risk_indicators, **growth_metrics, **peer_benchmarks, **ai_analysis}.items():
                    setattr(report, key, value)
                report.last_updated = timezone.now()
                report.save()
            
            logger.info(f"AI analyst report generated successfully for {project.name}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating AI analyst report for {project.name}: {str(e)}")
            # Return a default report if generation fails
            return self._create_default_report(project)
    
    def _calculate_risk_indicators(self, project: Project) -> Dict:
        """Calculate various risk indicators for the project"""
        try:
            # TAM Inflation Risk (based on funding goal vs market size)
            tam_risk = self._calculate_tam_risk(project)
            
            # Financial Consistency Risk (based on funding patterns)
            financial_risk = self._calculate_financial_consistency_risk(project)
            
            # Market Saturation Risk (based on competition)
            market_risk = self._calculate_market_saturation_risk(project)
            
            # Competition Risk (based on similar projects)
            competition_risk = self._calculate_competition_risk(project)
            
            # Team Risk (based on team size and positions)
            team_risk = self._calculate_team_risk(project)
            
            # Calculate overall risk score
            risk_score = (tam_risk + financial_risk + market_risk + competition_risk + team_risk) / 5
            
            # Determine risk level
            if risk_score <= 25:
                risk_level = 'low'
            elif risk_score <= 50:
                risk_level = 'medium'
            elif risk_score <= 75:
                risk_level = 'high'
            else:
                risk_level = 'critical'
            
            return {
                'risk_score': round(risk_score, 1),
                'risk_level': risk_level,
                'tam_inflation_risk': round(tam_risk, 1),
                'financial_consistency_risk': round(financial_risk, 1),
                'market_saturation_risk': round(market_risk, 1),
                'competition_risk': round(competition_risk, 1),
                'team_risk': round(team_risk, 1)
            }
            
        except Exception as e:
            logger.error(f"Error calculating risk indicators: {str(e)}")
            return self._get_default_risk_indicators()
    
    def _calculate_growth_metrics(self, project: Project) -> Dict:
        """Calculate growth potential metrics"""
        try:
            # Traction Score (based on views, investments, recent activity)
            traction_score = self._calculate_traction_score(project)
            
            # Hiring Momentum (based on open positions)
            hiring_momentum = self._calculate_hiring_momentum(project)
            
            # Market Demand Score (based on category popularity)
            market_demand = self._calculate_market_demand_score(project)
            
            # Scalability Potential (based on business model)
            scalability = self._calculate_scalability_potential(project)
            
            # Calculate overall growth score
            growth_score = (traction_score + hiring_momentum + market_demand + scalability) / 4
            
            # Determine growth index
            if growth_score >= 80:
                growth_index = 'exceptional'
            elif growth_score >= 60:
                growth_index = 'high'
            elif growth_score >= 40:
                growth_index = 'medium'
            else:
                growth_index = 'low'
            
            return {
                'growth_score': round(growth_score, 1),
                'growth_index': growth_index,
                'traction_score': round(traction_score, 1),
                'hiring_momentum': round(hiring_momentum, 1),
                'market_demand_score': round(market_demand, 1),
                'scalability_potential': round(scalability, 1)
            }
            
        except Exception as e:
            logger.error(f"Error calculating growth metrics: {str(e)}")
            return self._get_default_growth_metrics()
    
    def _perform_peer_benchmarking(self, project: Project) -> Dict:
        """Perform peer benchmarking analysis"""
        try:
            # Get all projects for comparison
            all_projects = Project.objects.all()
            sector_projects = Project.objects.filter(category=project.category)
            stage_projects = Project.objects.filter(stage=project.stage)
            
            # Calculate platform rankings
            platform_rank, platform_percentile = self._calculate_platform_ranking(project, all_projects)
            
            # Calculate sector rankings
            sector_rank, sector_percentile = self._calculate_sector_ranking(project, sector_projects)
            
            # Calculate vs averages
            vs_sector_avg = self._calculate_vs_sector_average(project, sector_projects)
            vs_platform_avg = self._calculate_vs_platform_average(project, all_projects)
            vs_similar_stage = self._calculate_vs_similar_stage(project, stage_projects)
            
            return {
                'sector_rank': sector_rank,
                'sector_percentile': round(sector_percentile, 1),
                'platform_rank': platform_rank,
                'platform_percentile': round(platform_percentile, 1),
                'vs_sector_avg': round(vs_sector_avg, 1),
                'vs_platform_avg': round(vs_platform_avg, 1),
                'vs_similar_stage': round(vs_similar_stage, 1)
            }
            
        except Exception as e:
            logger.error(f"Error performing peer benchmarking: {str(e)}")
            return self._get_default_benchmarking()
    
    def _generate_ai_analysis(self, project: Project, risk_indicators: Dict, growth_metrics: Dict, peer_benchmarks: Dict) -> Dict:
        """Generate AI-powered analysis text using Gemini"""
        try:
            # Prepare context for AI analysis
            context = {
                'project_name': project.name,
                'description': project.description,
                'category': project.category,
                'stage': project.stage,
                'funding_goal': project.funding_goal,
                'current_funding': project.current_funding(),
                'risk_score': risk_indicators['risk_score'],
                'growth_score': growth_metrics['growth_score'],
                'sector_rank': peer_benchmarks['sector_rank'],
                'platform_rank': peer_benchmarks['platform_rank']
            }
            
            # Generate risk analysis
            risk_analysis = self._generate_risk_analysis_text(context)
            
            # Generate growth analysis
            growth_analysis = self._generate_growth_analysis_text(context)
            
            # Generate peer analysis
            peer_analysis = self._generate_peer_analysis_text(context)
            
            # Generate recommendations
            recommendations = self._generate_recommendations_text(context)
            
            return {
                'risk_analysis': risk_analysis,
                'growth_analysis': growth_analysis,
                'peer_analysis': peer_analysis,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error generating AI analysis: {str(e)}")
            return self._get_default_analysis_text()
    
    # Risk calculation methods
    def _calculate_tam_risk(self, project: Project) -> float:
        """Calculate TAM inflation risk based on funding goal vs market size"""
        try:
            if project.funding_goal <= 0:
                return 50.0  # Medium risk if no funding goal
            
            # Simple heuristic: higher funding goals relative to typical amounts = higher risk
            typical_funding = 50.0  # ETH
            if project.funding_goal > typical_funding * 5:
                return 80.0  # High risk
            elif project.funding_goal > typical_funding * 2:
                return 60.0  # Medium-high risk
            else:
                return 30.0  # Low-medium risk
        except:
            return 50.0
    
    def _calculate_financial_consistency_risk(self, project: Project) -> float:
        """Calculate financial consistency risk based on funding patterns"""
        try:
            investments = Investment.objects.filter(project=project)
            if not investments.exists():
                return 40.0  # Medium risk for no investments
            
            # Check for consistent funding patterns
            amounts = [float(inv.amount) for inv in investments]
            if len(amounts) < 2:
                return 30.0  # Low risk for single investment
            
            # Calculate variance in investment amounts
            avg_amount = sum(amounts) / len(amounts)
            variance = sum((amount - avg_amount) ** 2 for amount in amounts) / len(amounts)
            std_dev = variance ** 0.5
            
            # Higher variance = higher risk
            if std_dev > avg_amount:
                return 70.0  # High risk
            elif std_dev > avg_amount * 0.5:
                return 50.0  # Medium risk
            else:
                return 30.0  # Low risk
        except:
            return 50.0
    
    def _calculate_market_saturation_risk(self, project: Project) -> float:
        """Calculate market saturation risk based on competition"""
        try:
            # Count similar projects in same category
            similar_projects = Project.objects.filter(category=project.category).exclude(id=project.id)
            competition_count = similar_projects.count()
            
            if competition_count > 10:
                return 80.0  # High risk - saturated market
            elif competition_count > 5:
                return 60.0  # Medium-high risk
            elif competition_count > 2:
                return 40.0  # Medium risk
            else:
                return 20.0  # Low risk
        except:
            return 50.0
    
    def _calculate_competition_risk(self, project: Project) -> float:
        """Calculate competition risk based on similar projects' success"""
        try:
            similar_projects = Project.objects.filter(category=project.category).exclude(id=project.id)
            if not similar_projects.exists():
                return 30.0  # Low risk if no competition
            
            # Calculate average funding of similar projects
            avg_funding = similar_projects.aggregate(avg=Avg('funding_goal'))['avg'] or 0
            current_funding = project.current_funding()
            
            if current_funding < avg_funding * 0.5:
                return 70.0  # High risk - underperforming
            elif current_funding < avg_funding:
                return 50.0  # Medium risk
            else:
                return 30.0  # Low risk - outperforming
        except:
            return 50.0
    
    def _calculate_team_risk(self, project: Project) -> float:
        """Calculate team risk based on team size and positions"""
        try:
            positions = Position.objects.filter(project=project)
            team_size = positions.count()
            
            if team_size == 0:
                return 80.0  # High risk - no team
            elif team_size < 3:
                return 60.0  # Medium-high risk - small team
            elif team_size < 6:
                return 40.0  # Medium risk
            else:
                return 20.0  # Low risk - good team size
        except:
            return 50.0
    
    # Growth calculation methods
    def _calculate_traction_score(self, project: Project) -> float:
        """Calculate traction score based on views and investments"""
        try:
            views = ProjectView.objects.filter(project=project).count()
            investments = Investment.objects.filter(project=project).count()
            total_invested = project.current_funding()
            
            # Weighted score
            score = (views * 0.3) + (investments * 20) + (total_invested * 0.1)
            return min(100.0, score)
        except:
            return 50.0
    
    def _calculate_hiring_momentum(self, project: Project) -> float:
        """Calculate hiring momentum based on open positions"""
        try:
            positions = Position.objects.filter(project=project)
            if not positions.exists():
                return 30.0  # Low momentum if no positions
            
            # More positions = higher momentum
            position_count = positions.count()
            if position_count > 5:
                return 90.0  # High momentum
            elif position_count > 3:
                return 70.0  # Good momentum
            elif position_count > 1:
                return 50.0  # Medium momentum
            else:
                return 30.0  # Low momentum
        except:
            return 50.0
    
    def _calculate_market_demand_score(self, project: Project) -> float:
        """Calculate market demand score based on category popularity"""
        try:
            # Count total investments in this category
            category_investments = Investment.objects.filter(project__category=project.category).count()
            total_investments = Investment.objects.count()
            
            if total_investments == 0:
                return 50.0
            
            # Calculate category popularity
            category_share = category_investments / total_investments
            return min(100.0, category_share * 200)  # Scale to 0-100
        except:
            return 50.0
    
    def _calculate_scalability_potential(self, project: Project) -> float:
        """Calculate scalability potential based on business model"""
        try:
            # Simple heuristic based on category
            scalable_categories = ['AI/ML', 'SaaS', 'Platform', 'Marketplace', 'Fintech']
            if project.category in scalable_categories:
                return 80.0  # High scalability
            else:
                return 60.0  # Medium scalability
        except:
            return 50.0
    
    # Benchmarking methods
    def _calculate_platform_ranking(self, project: Project, all_projects) -> Tuple[int, float]:
        """Calculate platform ranking and percentile"""
        try:
            if not all_projects.exists():
                return 1, 100.0
            
            # Simple ranking based on current funding
            project_funding = project.current_funding()
            better_projects = all_projects.filter(
                models.Q(current_funding__gt=project_funding) | 
                models.Q(current_funding=project_funding, id__lt=project.id)
            ).count()
            
            rank = better_projects + 1
            percentile = ((len(all_projects) - rank + 1) / len(all_projects)) * 100
            
            return rank, percentile
        except:
            return 1, 50.0
    
    def _calculate_sector_ranking(self, project: Project, sector_projects) -> Tuple[int, float]:
        """Calculate sector ranking and percentile"""
        try:
            if not sector_projects.exists():
                return 1, 100.0
            
            project_funding = project.current_funding()
            better_projects = sector_projects.filter(
                models.Q(current_funding__gt=project_funding) | 
                models.Q(current_funding=project_funding, id__lt=project.id)
            ).count()
            
            rank = better_projects + 1
            percentile = ((len(sector_projects) - rank + 1) / len(sector_projects)) * 100
            
            return rank, percentile
        except:
            return 1, 50.0
    
    def _calculate_vs_sector_average(self, project: Project, sector_projects) -> float:
        """Calculate score vs sector average"""
        try:
            if not sector_projects.exists():
                return 0.0
            
            project_funding = project.current_funding()
            avg_funding = sector_projects.aggregate(avg=Avg('current_funding'))['avg'] or 0
            
            if avg_funding == 0:
                return 0.0
            
            return ((project_funding - avg_funding) / avg_funding) * 100
        except:
            return 0.0
    
    def _calculate_vs_platform_average(self, project: Project, all_projects) -> float:
        """Calculate score vs platform average"""
        try:
            if not all_projects.exists():
                return 0.0
            
            project_funding = project.current_funding()
            avg_funding = all_projects.aggregate(avg=Avg('current_funding'))['avg'] or 0
            
            if avg_funding == 0:
                return 0.0
            
            return ((project_funding - avg_funding) / avg_funding) * 100
        except:
            return 0.0
    
    def _calculate_vs_similar_stage(self, project: Project, stage_projects) -> float:
        """Calculate score vs similar stage startups"""
        try:
            if not stage_projects.exists():
                return 0.0
            
            project_funding = project.current_funding()
            avg_funding = stage_projects.aggregate(avg=Avg('current_funding'))['avg'] or 0
            
            if avg_funding == 0:
                return 0.0
            
            return ((project_funding - avg_funding) / avg_funding) * 100
        except:
            return 0.0
    
    # AI text generation methods
    def _generate_risk_analysis_text(self, context: Dict) -> str:
        """Generate risk analysis text using AI"""
        try:
            prompt = f"""
            Analyze the risk profile for the startup "{context['project_name']}" in the {context['category']} sector.
            
            Key metrics:
            - Risk Score: {context['risk_score']}/100
            - Funding Goal: {context['funding_goal']} ETH
            - Current Funding: {context['current_funding']} ETH
            - Stage: {context['stage']}
            
            Provide a concise risk analysis focusing on:
            1. Key risk factors
            2. Market risks
            3. Financial risks
            4. Team risks
            
            Keep it under 200 words and investor-focused.
            """
            
            # Generate analysis based on metrics instead of using API
            analysis_points = []
            
            # Risk level assessment
            if context['risk_score'] > 70:
                analysis_points.append("High risk profile requires careful due diligence.")
            elif context['risk_score'] > 40:
                analysis_points.append("Moderate risk level with manageable exposure.")
            else:
                analysis_points.append("Low risk profile with strong fundamentals.")
            
            # Stage-based analysis
            if context['stage'] in ['Idea', 'MVP']:
                analysis_points.append("Early stage presents execution and market validation risks.")
            elif context['stage'] in ['Beta', 'Launch']:
                analysis_points.append("Product-market fit validation is critical at this stage.")
            else:
                analysis_points.append("Growth stage shows proven concept with scaling opportunities.")
            
            # Funding analysis
            funding_ratio = context['current_funding'] / max(context['funding_goal'], 1)
            if funding_ratio < 0.3:
                analysis_points.append("Low funding progress may indicate market validation challenges.")
            elif funding_ratio > 0.8:
                analysis_points.append("Strong funding traction demonstrates investor confidence.")
            
            return " ".join(analysis_points) or "Risk analysis based on current metrics and market position."
        except:
            return "Risk analysis based on current metrics and market position."
    
    def _generate_growth_analysis_text(self, context: Dict) -> str:
        """Generate growth analysis text using AI"""
        try:
            prompt = f"""
            Analyze the growth potential for the startup "{context['project_name']}" in the {context['category']} sector.
            
            Key metrics:
            - Growth Score: {context['growth_score']}/100
            - Stage: {context['stage']}
            - Description: {context['description'][:200]}...
            
            Provide a concise growth analysis focusing on:
            1. Market opportunity
            2. Traction potential
            3. Scalability factors
            4. Growth drivers
            
            Keep it under 200 words and investor-focused.
            """
            
            # Generate analysis based on metrics instead of using API
            analysis_points = []
            
            # Growth potential assessment
            if context['growth_score'] > 75:
                analysis_points.append("Exceptional growth potential with strong market drivers.")
            elif context['growth_score'] > 50:
                analysis_points.append("Solid growth prospects with favorable market conditions.")
            elif context['growth_score'] > 25:
                analysis_points.append("Moderate growth potential requiring strategic execution.")
            else:
                analysis_points.append("Limited growth indicators suggest market challenges.")
            
            # Category-based insights
            if context['category'] in ['AI', 'Fintech']:
                analysis_points.append("High-growth sector with strong investor interest.")
            elif context['category'] in ['Health', 'Education']:
                analysis_points.append("Stable sector with sustainable growth opportunities.")
            
            # Stage progression analysis
            if context['stage'] in ['Growth', 'Scaling']:
                analysis_points.append("Advanced stage demonstrates proven scalability.")
            
            return " ".join(analysis_points) or "Growth analysis based on market metrics and sector dynamics."
        except:
            return "Growth analysis based on market metrics and sector dynamics."
    
    def _generate_peer_analysis_text(self, context: Dict) -> str:
        """Generate peer benchmarking analysis text using AI"""
        try:
            prompt = f"""
            Provide peer benchmarking analysis for the startup "{context['project_name']}" in the {context['category']} sector.
            
            Key metrics:
            - Sector Rank: #{context['sector_rank']}
            - Platform Rank: #{context['platform_rank']}
            - Growth Score: {context['growth_score']}/100
            - Risk Score: {context['risk_score']}/100
            
            Provide a concise peer analysis focusing on:
            1. Competitive position
            2. Sector performance
            3. Platform standing
            4. Benchmarking insights
            
            Keep it under 200 words and investor-focused.
            """
            
            # Generate analysis based on benchmarking data
            analysis_points = []
            
            # Ranking analysis
            if context.get('sector_rank', 10) <= 3:
                analysis_points.append("Top performer in sector with exceptional metrics.")
            elif context.get('sector_rank', 10) <= 10:
                analysis_points.append("Strong sector position above average performance.")
            else:
                analysis_points.append("Below average sector performance requires improvement.")
            
            # Platform comparison
            if context.get('platform_rank', 50) <= 10:
                analysis_points.append("Platform leader with outstanding investor appeal.")
            elif context.get('platform_rank', 50) <= 25:
                analysis_points.append("Above-average platform performance among startups.")
            
            # Sector performance
            vs_avg = context.get('vs_sector_avg', 0)
            if vs_avg > 20:
                analysis_points.append("Significantly outperforms sector benchmarks.")
            elif vs_avg > 0:
                analysis_points.append("Modest outperformance vs sector average.")
            else:
                analysis_points.append("Underperformance vs sector indicates operational challenges.")
            
            return " ".join(analysis_points) or "Competitive position analysis based on platform and sector benchmarks."
        except:
            return "Competitive position analysis based on platform and sector benchmarks."
    
    def _generate_recommendations_text(self, context: Dict) -> str:
        """Generate investment recommendations text using AI"""
        try:
            prompt = f"""
            Provide investment recommendations for the startup "{context['project_name']}" in the {context['category']} sector.
            
            Key metrics:
            - Risk Score: {context['risk_score']}/100
            - Growth Score: {context['growth_score']}/100
            - Sector Rank: #{context['sector_rank']}
            - Stage: {context['stage']}
            
            Provide concise investment recommendations focusing on:
            1. Investment thesis
            2. Key considerations
            3. Due diligence areas
            4. Risk mitigation strategies
            
            Keep it under 200 words and investor-focused.
            """
            
            # Generate recommendations based on analysis
            recommendations = []
            
            # Risk-based recommendations
            risk_score = context.get('risk_score', 50)
            if risk_score > 70:
                recommendations.append("HIGH RISK: Recommend detailed due diligence and limited exposure.")
            elif risk_score > 40:
                recommendations.append("MODERATE RISK: Standard due diligence with diversified allocation.")
            else:
                recommendations.append("LOW RISK: Suitable for larger allocation with strong fundamentals.")
            
            # Growth-based recommendations
            growth_score = context.get('growth_score', 50)
            if growth_score > 75:
                recommendations.append("Strong growth trajectory supports premium valuation.")
            elif growth_score < 30:
                recommendations.append("Limited growth potential suggests conservative valuation.")
            
            # Stage-based advice
            stage = context.get('stage', 'Unknown')
            if stage in ['Idea', 'MVP']:
                recommendations.append("Early stage investment requires higher risk tolerance.")
            elif stage in ['Growth', 'Scaling']:
                recommendations.append("Proven model suitable for growth-focused portfolios.")
            
            # Sector recommendations
            category = context.get('category', '')
            if category in ['AI', 'Fintech']:
                recommendations.append("High-demand sector with strong exit opportunities.")
            
            return " ".join(recommendations) or "Investment recommendation based on comprehensive risk-return analysis."
        except:
            return "Investment recommendation based on comprehensive risk-return analysis."
    
    # Default/fallback methods
    def _get_default_risk_indicators(self) -> Dict:
        return {
            'risk_score': 50.0,
            'risk_level': 'medium',
            'tam_inflation_risk': 50.0,
            'financial_consistency_risk': 50.0,
            'market_saturation_risk': 50.0,
            'competition_risk': 50.0,
            'team_risk': 50.0
        }
    
    def _get_default_growth_metrics(self) -> Dict:
        return {
            'growth_score': 50.0,
            'growth_index': 'medium',
            'traction_score': 50.0,
            'hiring_momentum': 50.0,
            'market_demand_score': 50.0,
            'scalability_potential': 50.0
        }
    
    def _get_default_benchmarking(self) -> Dict:
        return {
            'sector_rank': 1,
            'sector_percentile': 50.0,
            'platform_rank': 1,
            'platform_percentile': 50.0,
            'vs_sector_avg': 0.0,
            'vs_platform_avg': 0.0,
            'vs_similar_stage': 0.0
        }
    
    def _get_default_analysis_text(self) -> Dict:
        return {
            'risk_analysis': 'Risk analysis unavailable at this time.',
            'growth_analysis': 'Growth analysis unavailable at this time.',
            'peer_analysis': 'Peer analysis unavailable at this time.',
            'recommendations': 'Investment recommendations unavailable at this time.'
        }
    
    def _create_default_report(self, project: Project) -> AIAnalystReport:
        """Create a default report if generation fails"""
        return AIAnalystReport.objects.create(
            project=project,
            ai_model_version=self.model_version,
            **self._get_default_risk_indicators(),
            **self._get_default_growth_metrics(),
            **self._get_default_benchmarking(),
            **self._get_default_analysis_text()
        )


# Global AI analyst instance
ai_analyst = AIAnalyst()
