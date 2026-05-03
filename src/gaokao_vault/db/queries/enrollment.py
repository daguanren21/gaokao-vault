from __future__ import annotations

import json

import asyncpg


async def upsert_enrollment_plan(conn: asyncpg.Connection, data: dict) -> int:
    row = await conn.fetchrow(
        """
        WITH updated AS (
            UPDATE enrollment_plans
            SET batch_code = $6,
                batch_category = $7,
                batch_segment = $8,
                major_id = $10,
                plan_count = $11,
                duration = $12,
                tuition = $13,
                note = $14,
                major_group_code = $15,
                major_code_raw = $16,
                campus = $17,
                education_location = $18,
                selection_requirement = $19,
                physical_exam_limit = $20,
                single_subject_limit = $21,
                adjustment_rule = $22,
                program_type = $23,
                eligibility_requirements = $24,
                physical_exam_or_political_review = $25,
                political_review_requirement = $26,
                service_obligation = $27,
                data_source = $28,
                source_url = $29,
                source_updated_at = $30,
                quality_flags = $31,
                content_hash = $32,
                crawl_task_id = $33
            WHERE school_id = $1
              AND province_id = $2
              AND year = $3
              AND subject_category_id IS NOT DISTINCT FROM $4
              AND batch IS NOT DISTINCT FROM $5
              AND major_name IS NOT DISTINCT FROM $9
            RETURNING id
        ),
        inserted AS (
            INSERT INTO enrollment_plans (school_id, province_id, year, subject_category_id,
                batch, batch_code, batch_category, batch_segment, major_name, major_id, plan_count, duration, tuition, note,
                major_group_code, major_code_raw, campus, education_location,
                selection_requirement, physical_exam_limit, single_subject_limit,
                adjustment_rule, program_type, eligibility_requirements,
                physical_exam_or_political_review, political_review_requirement, service_obligation,
                data_source, source_url, source_updated_at, quality_flags,
                content_hash, crawl_task_id)
            SELECT $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28,$29,$30,$31,$32,$33
            WHERE NOT EXISTS (SELECT 1 FROM updated)
            RETURNING id
        )
        SELECT id FROM updated
        UNION ALL
        SELECT id FROM inserted
        LIMIT 1
        """,
        data["school_id"],
        data["province_id"],
        data["year"],
        data.get("subject_category_id"),
        data.get("batch"),
        data.get("batch_code"),
        data.get("batch_category"),
        data.get("batch_segment"),
        data.get("major_name"),
        data.get("major_id"),
        data.get("plan_count"),
        data.get("duration"),
        data.get("tuition"),
        data.get("note"),
        data.get("major_group_code"),
        data.get("major_code_raw"),
        data.get("campus"),
        data.get("education_location"),
        data.get("selection_requirement"),
        data.get("physical_exam_limit"),
        data.get("single_subject_limit"),
        data.get("adjustment_rule"),
        data.get("program_type"),
        data.get("eligibility_requirements"),
        data.get("physical_exam_or_political_review"),
        data.get("political_review_requirement"),
        data.get("service_obligation"),
        data.get("data_source"),
        data.get("source_url"),
        data.get("source_updated_at"),
        json.dumps(data.get("quality_flags", []), ensure_ascii=False),
        data.get("content_hash"),
        data.get("crawl_task_id"),
    )
    return row["id"]


async def upsert_charter(conn: asyncpg.Connection, data: dict) -> int:
    row = await conn.fetchrow(
        """
        INSERT INTO admission_charters (school_id, year, title, content, publish_date,
            source_url, content_hash, crawl_task_id)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
        ON CONFLICT (school_id, year) DO UPDATE SET
            title=EXCLUDED.title, content=EXCLUDED.content,
            publish_date=EXCLUDED.publish_date, source_url=EXCLUDED.source_url,
            content_hash=EXCLUDED.content_hash, crawl_task_id=EXCLUDED.crawl_task_id
        RETURNING id
        """,
        data["school_id"],
        data["year"],
        data.get("title"),
        data["content"],
        data.get("publish_date"),
        data.get("source_url"),
        data.get("content_hash"),
        data.get("crawl_task_id"),
    )
    return row["id"]


async def upsert_timeline(conn: asyncpg.Connection, data: dict) -> int:
    row = await conn.fetchrow(
        """
        INSERT INTO volunteer_timelines (province_id, year, batch, start_time, end_time, note,
            content_hash, crawl_task_id)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
        ON CONFLICT (province_id, year, batch) DO UPDATE SET
            start_time=EXCLUDED.start_time, end_time=EXCLUDED.end_time, note=EXCLUDED.note,
            content_hash=EXCLUDED.content_hash, crawl_task_id=EXCLUDED.crawl_task_id
        RETURNING id
        """,
        data["province_id"],
        data["year"],
        data["batch"],
        data.get("start_time"),
        data.get("end_time"),
        data.get("note"),
        data.get("content_hash"),
        data.get("crawl_task_id"),
    )
    return row["id"]
