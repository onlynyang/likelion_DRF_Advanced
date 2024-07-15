from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view): # 요청 수행 전
        return request.user and request.user.is_authenticated # request.user가 존재하고 인증된 사용자인 경우 True 반환
    
    def has_object_permission(self, request, view, obj): # 특정 객체에 대한 요청 수행 전
        if request.method in SAFE_METHODS: # 요청 메소드가 SAFE_METHODS 중 하나인 경우
            return True # Ture 반환 (요청허용)
        return obj.writer == request.user or request.user.is_authenticated # 그외의 메소드에서 '객체 작성자'='요청 사용자' or 사용자=superuser인 경우 True