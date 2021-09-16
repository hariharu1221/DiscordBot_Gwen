'''
    <config.py>
    봇의 설정을 이렇게 따로 빼 놓으면 편하게 설정할 수 있어요!
'''


class Config:
    # 봇의 토큰
    token = 'ODg1MDMwODQ2MDY5ODk5MjY0.YThHNA.nsKqk1W6AmNgsaTjDdo95n2pDok'
    # 디버그 모드가 켜졌을 때 사용할 토큰
    test_token = 'ODg1MDMwODQ2MDY5ODk5MjY0.YThHNA.nsKqk1W6AmNgsaTjDdo95n2pDok'

    # 디버그 여부
    is_debug = False

    # 상태 메시지
    activity = "가위가 바위를 이기게"

    # 접두사
    prefixes = ['#', '그웬아 ']

    # 봇의 버전
    version = '-1.0'

    # 관리자 디스코드 id
    admin = [758963978331619331]

    def using_token(self):
        ''' 사용해야 하는 봇 토큰을 반환합니다. '''
        return self.test_token if self.is_debug else self.token

    def prefixes_no_space(self):
        ''' 접두사들을 띄어쓰기 없이 반환합니다. '''
        return [i.replace(' ', '') for i in self.prefixes]
