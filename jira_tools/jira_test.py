from jira import JIRA

from jira_tools import JIRA_URL, EMAIL, API_TOKEN, account_gary, account_al

PROJECT = "OP"  # 運維
LABELS = ["Team:運維"]  # 添加標籤
REPORTER = {"accountId": account_gary}  # reporter
ASSIGNEE = {"accountId": account_al}  # 負責人


FEATURE_ID = "10024"
SUBTASK_ID = "10020"


def connect():
    # 設定 JIRA URL 和使用者認證
    jira_url = JIRA_URL
    email = EMAIL
    api_token = API_TOKEN

    # 連接到 JIRA
    return JIRA(server=jira_url, basic_auth=(email, api_token))


def create_issue(jira_connect):
    new_issue = jira_connect.create_issue(
        project=PROJECT,  # 運維
        labels=LABELS,  # 添加標籤
        summary="[OpsMgmt] test",  # 標題
        description="",  # 描述
        issuetype={"id": FEATURE_ID},
        # parent={"key": "OP-4361"},  # 後台重構
        # parent={"key": "OP-4469"},  # create cdn
        parent={"key": "OP-2144"},  # OpsMgmt
        reporter=REPORTER,
        assignee=ASSIGNEE,
    )
    print_msg(new_issue.key)


def create_sub_task(jira_connect, sub_task_summary: [str], parent_issue: str):
    for summary in sub_task_summary:
        new_issue = jira_connect.create_issue(
            project=PROJECT,  # 運維
            labels=LABELS,  # 添加標籤
            summary=f"[OpsMgmt] {summary}",  # 標題
            description="",  # 描述
            issuetype={"id": SUBTASK_ID},  # subtask 最小工作單位
            parent={"key": parent_issue},  # 設定父工單
            reporter=REPORTER,
            assignee=ASSIGNEE,
        )
        print_msg(new_issue.key)


def print_msg(key):
    print("新工單已建立，工單號碼為：", key)

    print(f"{JIRA_URL}/browse/{key}")

    print("[git 開分支]")

    print("git fetch --all")

    print(f"git checkout -b al.ma/{key} origin/main")


if __name__ == "__main__":
    conn = connect()

    # issue_key = "OP-4395"
    # issue_key = "OP-3840"
    # issue = conn.issue(issue_key)
    # print(issue)

    create_issue(conn)

    # create_sub_task(conn, ["al-gen-subTask"], "OP-4371")
