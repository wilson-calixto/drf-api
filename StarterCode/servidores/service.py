class ServidorService:

    @staticmethod
    def update(instance,validated_data):
        cursos = validated_data.pop("cursos", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if cursos is not None:
            instance.cursos.set(cursos)

        return instance
