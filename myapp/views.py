from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from django.http import HttpResponse
from .models import Resume
from .serializers import ResumeSerializer
import json

class ResumeViewSet(viewsets.ViewSet):
    def retrieve(self, request):
        resume, created = Resume.objects.get_or_create(user=request.user)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

    def partial_update(self, request):
        resume, created = Resume.objects.get_or_create(user=request.user)
        serializer = ResumeSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='export-pdf')
    def export_pdf(self, request):
        resume, created = Resume.objects.get_or_create(user=request.user)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title and Professional Title
        elements.append(Paragraph(f"{resume.full_name or 'Your Name'}", styles['Title']))
        if resume.title:
            elements.append(Paragraph(resume.title, styles['Heading2']))
        elements.append(Spacer(1, 12))

        # Contact Info
        contact_data = [
            ['Email:', resume.email or 'N/A'],
            ['Phone:', resume.phone or 'N/A'],
            ['Location:', resume.location or 'N/A'],
            ['Address:', resume.address or 'N/A'],
            ['LinkedIn:', resume.linkedin or 'N/A'],
            ['GitHub:', resume.github or 'N/A'],
            ['Portfolio:', resume.portfolio or 'N/A'],
        ]
        contact_table = Table(contact_data, colWidths=[100, 400])
        contact_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONT', (0,0), (-1,-1), 'Helvetica', 10),
        ]))
        elements.append(Paragraph("Contact Information", styles['Heading2']))
        elements.append(contact_table)
        elements.append(Spacer(1, 12))

        # Summary
        if resume.objective:
            elements.append(Paragraph("Summary", styles['Heading2']))
            elements.append(Paragraph(resume.objective.replace('\n', '<br/>'), styles['BodyText']))
            elements.append(Spacer(1, 12))

        # Education
        try:
            education = json.loads(resume.education) if resume.education else []
        except json.JSONDecodeError:
            education = []
        if education:
            elements.append(Paragraph("Education", styles['Heading2']))
            for edu in education:
                elements.append(Paragraph(f"{edu.get('degree', '')}, {edu.get('field', '')}", styles['BodyText']))
                elements.append(Paragraph(edu.get('institution', ''), styles['BodyText']))
                elements.append(Paragraph(f"{edu.get('startDate', '')} - {edu.get('endDate', '')}", styles['BodyText']))
                elements.append(Spacer(1, 6))
            elements.append(Spacer(1, 12))

        # Experience
        try:
            experience = json.loads(resume.experience) if resume.experience else []
        except json.JSONDecodeError:
            experience = []
        if experience:
            elements.append(Paragraph("Work Experience", styles['Heading2']))
            for exp in experience:
                elements.append(Paragraph(f"{exp.get('position', '')}", styles['BodyText']))
                elements.append(Paragraph(exp.get('company', ''), styles['BodyText']))
                elements.append(Paragraph(f"{exp.get('startDate', '')} - {exp.get('endDate', '')}", styles['BodyText']))
                elements.append(Paragraph(exp.get('description', '').replace('\n', '<br/>'), styles['BodyText']))
                elements.append(Spacer(1, 6))
            elements.append(Spacer(1, 12))

        # Projects
        try:
            projects = json.loads(resume.projects) if resume.projects else []
        except json.JSONDecodeError:
            projects = []
        if projects:
            elements.append(Paragraph("Projects", styles['Heading2']))
            for proj in projects:
                elements.append(Paragraph(proj.get('name', ''), styles['BodyText']))
                elements.append(Paragraph(f"{proj.get('startDate', '')} - {proj.get('endDate', '')}", styles['BodyText']))
                elements.append(Paragraph(proj.get('description', '').replace('\n', '<br/>'), styles['BodyText']))
                elements.append(Paragraph(f"Technologies: {', '.join(proj.get('technologies', []))}", styles['BodyText']))
                elements.append(Spacer(1, 6))
            elements.append(Spacer(1, 12))

        # Other sections
        sections = [
            ('Skills', resume.skills),
            ('Languages', resume.languages),
            ('Certifications', resume.certifications),
            ('Awards', resume.awards),
            ('Organizations', resume.organizations),
            ('Co-curricular Activities', resume.coCurricular),
            ('Declaration', resume.declarations),
        ]
        for title, content in sections:
            if content:
                elements.append(Paragraph(title, styles['Heading2']))
                elements.append(Paragraph(content.replace('\n', '<br/>'), styles['BodyText']))
                elements.append(Spacer(1, 12))

        doc.build(elements)
        return response