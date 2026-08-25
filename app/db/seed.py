from datetime import datetime, timedelta, timezone

from app.db.database import SessionLocal

from app.models.users import User

from app.models.campaigns import (
    Campaign,
    CampaignMember,
    CampaignTask
)

from app.core.security import hash_password


def seed():
    db = SessionLocal()

    try:
        # =========================
        # 1. USERS
        # =========================

        users_data = [
            {
                "email": "owner@gmail.com",
                "full_name": "Campaign Owner",
                "password": "123456",
                "role": "USER"
            },
            {
                "email": "content@gmail.com",
                "full_name": "Content Member",
                "password": "123456",
                "role": "USER"
            },
            {
                "email": "ads@gmail.com",
                "full_name": "Ads Member",
                "password": "123456",
                "role": "USER"
            },
            {
                "email": "design@gmail.com",
                "full_name": "Design Member",
                "password": "123456",
                "role": "USER"
            },
            {
                "email": "member@gmail.com",
                "full_name": "Normal Member",
                "password": "123456",
                "role": "USER"
            },
            {
                "email": "outside@gmail.com",
                "full_name": "Outside User",
                "password": "123456",
                "role": "USER"
            }
        ]

        users = {}

        for data in users_data:
            user = db.query(User).filter(
                User.email == data["email"]
            ).first()

            if user is None:
                user = User(
                    email=data["email"],
                    full_name=data["full_name"],
                    password_hash=hash_password(data["password"]),
                    role=data["role"],
                    is_active=True
                )

                db.add(user)
                db.flush()

            users[data["email"]] = user

        # =========================
        # 2. CAMPAIGN
        # =========================

        owner = users["owner@gmail.com"]

        campaign = db.query(Campaign).filter(
            Campaign.name == "Chiến dịch Marketing Mùa Hè 2026"
        ).first()

        if campaign is None:
            campaign = Campaign(
                name="Chiến dịch Marketing Mùa Hè 2026",
                description="Chiến dịch marketing mẫu phục vụ test và demo Campaign Management.",
                owner_id=owner.id
            )

            db.add(campaign)
            db.flush()

        # =========================
        # 3. CAMPAIGN MEMBERS
        # =========================

        members_data = [
            {
                "email": "owner@gmail.com",
                "role": "OWNER",
                "position": "CONTENT"
            },
            {
                "email": "content@gmail.com",
                "role": "MEMBER",
                "position": "CONTENT"
            },
            {
                "email": "ads@gmail.com",
                "role": "MEMBER",
                "position": "ADS"
            },
            {
                "email": "design@gmail.com",
                "role": "MEMBER",
                "position": "DESIGN"
            },
            {
                "email": "member@gmail.com",
                "role": "MEMBER",
                "position": "CONTENT"
            }
        ]

        for data in members_data:
            user = users[data["email"]]

            member = db.query(CampaignMember).filter(
                CampaignMember.campaign_id == campaign.id,
                CampaignMember.user_id == user.id
            ).first()

            if member is None:
                member = CampaignMember(
                    campaign_id=campaign.id,
                    user_id=user.id,
                    role=data["role"],
                    position=data["position"]
                )

                db.add(member)

        db.flush()

        # =========================
        # 4. CAMPAIGN TASKS
        # =========================

        content_user = users["content@gmail.com"]
        ads_user = users["ads@gmail.com"]
        design_user = users["design@gmail.com"]

        now = datetime.now(timezone.utc)

        tasks_data = [
            {
                "title": "Viết nội dung Facebook",
                "description": "Viết nội dung giới thiệu chiến dịch và sản phẩm.",
                "assignee_id": content_user.id,
                "status": "TODO",
                "priority": "HIGH",
                "due_date": now + timedelta(days=3)
            },
            {
                "title": "Chạy quảng cáo Facebook",
                "description": "Thiết lập và theo dõi quảng cáo Facebook.",
                "assignee_id": ads_user.id,
                "status": "IN_PROGRESS",
                "priority": "HIGH",
                "due_date": now + timedelta(days=5)
            },
            {
                "title": "Thiết kế banner",
                "description": "Thiết kế banner cho chiến dịch marketing.",
                "assignee_id": design_user.id,
                "status": "DONE",
                "priority": "MEDIUM",
                "due_date": now - timedelta(days=1)
            },
            {
                "title": "Lập kế hoạch nội dung",
                "description": "Lập lịch đăng bài cho toàn bộ chiến dịch.",
                "assignee_id": content_user.id,
                "status": "TODO",
                "priority": "LOW",
                "due_date": now + timedelta(days=7)
            },
            {
                "title": "Kiểm tra hiệu quả quảng cáo",
                "description": "Theo dõi CTR, CPC và số lượt chuyển đổi.",
                "assignee_id": ads_user.id,
                "status": "IN_PROGRESS",
                "priority": "MEDIUM",
                "due_date": now + timedelta(days=4)
            },
            {
                "title": "Thiết kế hình ảnh Instagram",
                "description": "Thiết kế bộ hình ảnh đăng Instagram.",
                "assignee_id": design_user.id,
                "status": "TODO",
                "priority": "LOW",
                "due_date": now + timedelta(days=8)
            }
        ]

        for data in tasks_data:
            task = db.query(CampaignTask).filter(
                CampaignTask.campaign_id == campaign.id,
                CampaignTask.title == data["title"]
            ).first()

            if task is None:
                task = CampaignTask(
                    campaign_id=campaign.id,
                    assignee_id=data["assignee_id"],
                    title=data["title"],
                    description=data["description"],
                    due_date=data["due_date"],
                    status=data["status"],
                    priority=data["priority"]
                )

                db.add(task)

        db.commit()

        print("===================================")
        print("SEED DATA THANH CONG")
        print("===================================")

        print("\nUSERS:")
        print("owner@gmail.com   / 123456")
        print("content@gmail.com / 123456")
        print("ads@gmail.com     / 123456")
        print("design@gmail.com  / 123456")
        print("member@gmail.com  / 123456")
        print("outside@gmail.com / 123456")

        print("\nCAMPAIGN:")
        print("Chiến dịch Marketing Mùa Hè 2026")

        print("\nTASKS:")
        print("- TODO")
        print("- IN_PROGRESS")
        print("- DONE")

        print("\nPRIORITY:")
        print("- LOW")
        print("- MEDIUM")
        print("- HIGH")

        print("\n===================================")

    except Exception as e:
        db.rollback()
        print("SEED DATA THAT BAI")
        print("ERROR:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed()