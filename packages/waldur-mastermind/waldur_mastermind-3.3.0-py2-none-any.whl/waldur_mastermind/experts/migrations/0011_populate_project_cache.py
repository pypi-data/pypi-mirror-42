# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-25 09:56
from __future__ import unicode_literals

from django.db import migrations


def populate_expert_request_initial_cache(apps, schema_editor):
    ExpertRequest = apps.get_model('experts', 'ExpertRequest')

    for request in ExpertRequest.objects.all():
        request.project_name = request.project.name
        request.project_uuid = request.project.uuid
        request.customer = request.project.customer
        request.save(update_fields=('project_name', 'project_uuid', 'customer'))


def populate_expert_contract_initial_cache(apps, schema_editor):
    ExpertContract = apps.get_model('experts', 'ExpertContract')

    for contract in ExpertContract.objects.all():
        contract.team_name = contract.team.name
        contract.team_uuid = contract.team.uuid
        contract.team_customer = contract.team.customer
        contract.save(update_fields=('team_name', 'team_uuid', 'team_customer'))


class Migration(migrations.Migration):

    dependencies = [
        ('experts', '0010_preserve_deleted_project_data'),
    ]

    operations = [
        migrations.RunPython(populate_expert_request_initial_cache),
        migrations.RunPython(populate_expert_contract_initial_cache),
    ]
