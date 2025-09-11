import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from models.portfolio import Portfolio, Personal, Skills, Experience, Project, Certification, Contact, Education, Skill
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_portfolio_data():
    """Seed the database with initial portfolio data"""
    
    # Check if portfolio already exists
    existing = await db.portfolio.find_one({})
    if existing:
        print("Portfolio data already exists. Skipping seed.")
        return
    
    # Create portfolio data
    portfolio = Portfolio(
        personal=Personal(
            name="Albee John",
            tagline="Data Analyst & Science Enthusiast",
            description="Passionate about transforming raw data into actionable insights through advanced analytics, data analysis, and data-driven decision making.",
            email="albeejohnwwe@gmail.com",
            phone="+91 8943785705",
            location="Kollam, Kerala",
            bio="""I am an aspiring data analyst, fascinated with the expanse of data analytics and data science technologies. 
            Currently pursuing expertise in Data Analysis and advanced analytics while building strong foundations in statistical analysis and data modeling.
            My journey spans from academic excellence to practical implementation, with experience in consulting and complex data analysis.
            
            I believe in the power of data to drive meaningful insights and strategic decision-making. My goal is to contribute 
            to innovative data-driven projects that solve real-world problems through advanced analytics and data analysis applications.""",
            education=[
                Education(
                    degree="B.Tech, Computer Science & Engineering",
                    institution="St. Thomas College Of Engineering & Technology",
                    period="2020-2024",
                    grade="Completed"
                ),
                Education(
                    degree="Senior Secondary (XII)",
                    institution="St. Gregorius Higher Secondary School, Kottarakkara",
                    period="2019",
                    grade="69.00%"
                ),
                Education(
                    degree="Secondary (X)",
                    institution="St. Mary's Bethany Central School, Valakom",
                    period="2016",
                    grade="CGPA: 9.60/10"
                )
            ]
        ),
        skills=Skills(
            technical=[
                Skill(name="Python", level=90, category="Programming"),
                Skill(name="R Programming", level=75, category="Programming"),
                Skill(name="SQL", level=85, category="Programming"),
                Skill(name="Data Analysis", level=90, category="Analytics"),
                Skill(name="Statistical Analysis", level=85, category="Analytics"),
                Skill(name="Data Visualization", level=85, category="Analytics"),
                Skill(name="Business Intelligence", level=80, category="Analytics"),
                Skill(name="Data Modeling", level=80, category="Analytics")
            ],
            tools=["NumPy", "Matplotlib", "Seaborn", "Pandas", "Excel", "Jupyter", "Tableau", "Power BI", "Google Analytics"],
            soft=["Effective Communication", "Teamwork", "Time Management", "Data Management", "Problem Solving", "Critical Thinking", "Statistical Reasoning", "Business Acumen"]
        ),
        experience=[
            Experience(
                title="Consultant",
                company="RM Plc",
                location="Thiruvananthapuram",
                period="May 2025 - Jul 2025",
                type="Contract",
                achievements=[
                    "Contributed high target within stipulated time limit",
                    "Handled complex data analysis and management",
                    "Improved time management processes",
                    "Developed accurate data management systems",
                    "Enhanced team collaboration and communication"
                ],
                technologies=["Data Analysis", "Project Management", "Team Collaboration"]
            )
        ],
        projects=[
            Project(
                name="Private Line: IMDB YouTube Clone",
                description="A comprehensive full-stack web application that combines the functionality of IMDB and YouTube, built using the MERN stack. Features include user authentication, video streaming, movie ratings, reviews, and a responsive design.",
                technologies=["MongoDB", "Express.js", "React", "Node.js", "JWT Authentication", "Video Streaming"],
                period="May 2023 - May 2024",
                status="Completed",
                highlights=[
                    "Developed a scalable full-stack application using MERN stack",
                    "Implemented user authentication and authorization",
                    "Created responsive UI with modern design principles",
                    "Integrated video streaming and movie database functionality",
                    "Collaborated effectively within a development team"
                ],
                github="#",
                demo="#"
            )
        ],
        certifications=[
            Certification(
                name="Data Analysis With Python And Advanced Analytics",
                issuer="Soften Technologies",
                period="Aug 2024 - Mar 2025",
                type="Virtual",
                description="Comprehensive coursework in Data Analysis using Python, integrating advanced analytics techniques and business intelligence applications, utilizing libraries such as NumPy, Matplotlib, Seaborn and more."
            )
        ],
        contact=Contact(
            email="albeejohnwwe@gmail.com",
            phone="+91 8943785705",
            location="Kollam, Kerala",
            availability="Open to opportunities",
            social={
                "linkedin": "#",
                "github": "#",
                "twitter": "#"
            }
        ),
        activities=[
            "IEEE Society Member - Active college member focusing on engineering innovation and data analysis networking",
            "Continuous learner in emerging data analytics technologies and industry trends",
            "Regular participant in data analysis meetups and analytics communities"
        ]
    )
    
    # Insert portfolio data
    result = await db.portfolio.insert_one(portfolio.dict())
    
    if result.inserted_id:
        print("✅ Portfolio data seeded successfully!")
    else:
        print("❌ Failed to seed portfolio data")

async def main():
    await seed_portfolio_data()
    client.close()

if __name__ == "__main__":
    asyncio.run(main())