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
        # Solo el admin ve todos los usuarios
        if user.is_superuser or user.roles.filter(nombre='Administrador').exists():
            return Usuario.objects.all()
        # Usuarios normales solo se ven a sí mismos
        return Usuario.objects.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        # Solo admin puede crear usuarios
        user = request.user
        if not (user.is_superuser or user.roles.filter(nombre='Administrador').exists()):
            return Response({'detail': 'Solo el administrador puede crear usuarios.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        password = data.pop('password', None)
        roles_ids = data.pop('roles', [])
        
        if not password:
            return Response({'detail': 'La contraseña es obligatoria.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si los roles vienen como lista de IDs
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

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Devuelve el perfil del usuario logueado con sus roles."""
        serializer = self.get_serializer(request.user)
        data = serializer.data
        # Agregar bandera is_admin para facilitar al frontend
        data['is_admin'] = request.user.is_superuser or request.user.roles.filter(nombre='Administrador').exists()
        return Response(data)


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]


class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    permission_classes = [IsAuthenticated]