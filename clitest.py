import click as cl
import re
from logger import setup_logger

logger = setup_logger("cli")


"""
أداة واجهة سطر الأوامر (CLI) لسحب بيانات TikTok Ads.

تتيح هذه الأداة سحب البيانات بشكل مباشر من الطرفية بدلاً من الجدولة التلقائية.
تتطلب المعالجة تحديد المتغيرات التالية:
1. رقم الحساب الإعلاني (Advertiser ID).
2. المدى الزمني (Time Range): [يومي، أسبوعي، شهري].
3. مستوى السحب (Level): [حملة، مجموعة إعلانية، إعلان].

المنطق البرمجي:
- التحقق من صحة رقم الحساب: معالجة حالات الخطأ في الإدخال أو عدم وجود صلاحيات.
- بناء الرابط بشكل ديناميكي بناءً على رقم الحساب المعتمد.
- توفير خيارات اختيار (Options) للمدى الزمني ومستوى السحب لضمان دقة البيانات.

الوظائف المطلوبة:
- دالة للتحقق من الأخطاء الإملائية لرقم الحساب.
- تعريف خيارات CLI (click options) للمتغيرات الثلاثة.
"""


def accountid_validation(ctx, param, value):
    regex = r"^\d{19}$"
    if not bool(re.match(regex, value)):
        raise cl.BadParameter(
            "the account id is not valid, please enter 19 charcher id which you have access on!"
        )
    return value


@cl.command()
@cl.option("--account_id", callback=accountid_validation, required=True)
@cl.option("--time_window", type=cl.Choice(["1", "2", "3", "4"]), default="1")
@cl.option(
    "--analysis_level",
    type=cl.Choice(["campaign", "adgroup", "ad"]),
    default="campaign",
)
@cl.option("--open_window", is_flag=True, default=False)
def final_url(account_id, time_window, analysis_level, open_window):
    logger.info(f"Executing CLI command with account_id={account_id}, time_window={time_window}, analysis_level={analysis_level}")
    finaUrl = f"https://ads.tiktok.com/i18n/manage/{analysis_level}?aadvid={account_id}&relative_time={time_window}"
    cl.echo(f"final url is {finaUrl}")
    logger.info(f"Generated URL: {finaUrl}")


if __name__ == "__main__":
    final_url()
