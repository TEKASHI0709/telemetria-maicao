from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Rol, Recurso
from .serializers import UsuarioSerializer, RolSerializer, RecursoSerializer

Usuario = get_user_model()


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.roles.filter(nombre='Administrador').exists():
            return Usuario.objects.all()
        return Usuario.objects.filter(id=user.id)

    def is_admin(self, user):
        return user.is_superuser or user.roles.filter(nombre='Administrador').exists()

    def create(self, request, *args, **kwargs):
        if not self.is_admin(request.user):
            return Response({'detail': 'Solo el administrador puede crear usuarios.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        password = data.pop('password', None)
        roles_ids = data.pop('roles', [])

        if not password:
            return Response({'detail': 'La contraseña es obligatoria.'}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(roles_ids, list) and roles_ids and isinstance(roles_ids[0], list):
            roles_ids = roles_ids[0]

        new_user = Usuario.objects.create(
            username=data.get('username'),
            email=data.get('email', ''),
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido', ''),
            is_active=data.get('is_active', True)
        )
        new_user.set_password(password)
        new_user.save()

        if roles_ids:
            new_user.roles.set(roles_ids)

        serializer = self.get_serializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not self.is_admin(request.user):
            return Response({'detail': 'Solo el administrador puede editar usuarios.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self.is_admin(request.user):
            return Response({'detail': 'Solo el administrador puede editar usuarios.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='reset-password')
    def reset_password(self, request, pk=None):
        if not self.is_admin(request.user):
            return Response({'detail': 'Solo el administrador puede resetear contraseñas.'}, status=status.HTTP_403_FORBIDDEN)

        user = self.get_object()
        new_password = request.data.get('new_password', '').strip()

        if not new_password or len(new_password) < 6:
            return Response({'detail': 'La contraseña debe tener al menos 6 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        from system_logs.models import SystemLog
        SystemLog.objects.create(
            log_type='USER_UPDATED',
            level='WARNING',
            message=f'Contraseña del usuario "{user.username}" reseteada por el administrador',
            user=user,
            metadata={'action': 'password_reset', 'admin': request.user.username}
        )

        return Response({'detail': 'Contraseña actualizada correctamente.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        user = request.user
        current_password = request.data.get('current_password', '').strip()
        new_password = request.data.get('new_password', '').strip()

        if not current_password or not new_password:
            return Response({'detail': 'Debes proporcionar la contraseña actual y la nueva.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({'detail': 'La contraseña actual es incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 6:
            return Response({'detail': 'La nueva contraseña debe tener al menos 6 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        from system_logs.models import SystemLog
        SystemLog.objects.create(
            log_type='USER_UPDATED',
            level='INFO',
            message=f'Usuario "{user.username}" cambió su contraseña',
            user=user,
            metadata={'action': 'self_password_change'}
        )

        return Response({'detail': 'Contraseña actualizada correctamente.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='update-profile')
    def update_profile(self, request):
        user = request.user
        nombre = request.data.get('nombre', '').strip()
        apellido = request.data.get('apellido', '').strip()
        email = request.data.get('email', '').strip()

        if nombre:
            user.nombre = nombre
        if apellido:
            user.apellido = apellido
        if email:
            user.email = email

        user.save()

        serializer = self.get_serializer(user)
        data = serializer.data
        data['is_admin'] = self.is_admin(user)
        return Response(data)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        data = serializer.data
        data['is_admin'] = self.is_admin(request.user)
        return Response(data)


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]


class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    permission_classes = [IsAuthenticated]