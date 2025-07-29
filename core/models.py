from tortoise.models import Model

from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    phone = fields.CharField(20, description="手机号", null=False, default="")
    avatar = fields.CharField(255, description="头像", null=False, default="")
    username = fields.CharField(50, description="名称", null=False, default="")
    nickname = fields.CharField(50, description="昵称", null=False, default="")
    password = fields.CharField(50, description="密码", null=False, default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

    def to_dict(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "avatar": self.avatar,
            "username": self.username,
            "nickname": self.nickname,
            "password": self.password,
            "created_at": self.created_at.isoformat()
        }


class Task(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    priority = fields.IntField(default=0)
    status = fields.IntField(default=1)  # 1=待执行,2=执行中,3=成功,4=失败
    owner = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "tasks"
        indexes = [("status", "created_at")]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "owner": self.owner,
            "created_at": self.created_at.isoformat()
        }
